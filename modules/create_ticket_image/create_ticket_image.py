import os
import sys
import structlog
from configparser import ConfigParser

import docopt
import qrcode
from PIL import Image, ImageDraw, ImageFont
import gspread
from oauth2client.service_account import ServiceAccountCredentials

logger=structlog.getLogger()

#設定ファイルの読み込み
CONF_FILE_NAME="./settings.conf"

def read_conf(fname=CONF_FILE_NAME,encoding="utf8"):
    config=ConfigParser()
    config.read(CONF_FILE_NAME,encoding=encoding)
    config_data={}
    for key in config:
        config_data.update(config[key])
    return config_data

config_data=read_conf()
msg=f"設定ファイルを読み込みました。{str(config_data)}"
logger.info(msg)

# ===== 設定 =====
DEF_SPREADSHEET_KEY = config_data.get("spreadsheet_key")
DEF_SHEET_NAME = config_data.get("sheet_name")
OUTPUT_DIR = config_data.get("output_dir")
DEF_IMAGE_TEMPLATE_PATH=config_data.get("image_template_path")

# 画像内の配置位置（テンプレに合わせて座標調整）
IMAGE_SIZE=config_data.get("image_size") or "1080,1920"
IMAGE_SIZE=list(map(int,IMAGE_SIZE.split(",",1)))
NAME_REL_REFT_UNDER_POS=config_data.get("name_rel_reft_under_pos") or "472,222"
NAME_REL_REFT_UNDER_POS=list(map(int,NAME_REL_REFT_UNDER_POS.split(",",1)))
NAME_POS = (    # 名前テキスト描画位置
    NAME_REL_REFT_UNDER_POS[0],
    IMAGE_SIZE[1]-NAME_REL_REFT_UNDER_POS[1]
)
NAME_FONT=ImageFont.truetype("meiryo.ttc",size=32)
ID_REL_LEFT_UNDER_POS=config_data.get("id_rel_left_under_pos") or "327,213"
ID_REL_LEFT_UNDER_POS=list(map(int,ID_REL_LEFT_UNDER_POS.split(",",1)))
ID_POS=(    # 会員番号テキスト描画位置
    ID_REL_LEFT_UNDER_POS[0],
    IMAGE_SIZE[1]-ID_REL_LEFT_UNDER_POS[1]
)
ID_FONT=ImageFont.truetype("arial.ttf",size=24)
QR_POS=config_data.get("qr_pos") or "747, 1571"          # QRコード左上座標
QR_POS=list(map(int,QR_POS.split(",",1)))
QR_SIZE = int(config_data.get("qr_size") or 232)              # QRコードの一辺ピクセル

# ===== スプシ認証・読み込み =====
DEF_KEYFILE=config_data.get("keyfile")
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]


def get_client(keyfile=DEF_KEYFILE):
    CREDS= ServiceAccountCredentials.from_json_keyfile_name(
        keyfile, scope
    )
    return gspread.authorize(CREDS)

def create_qrcode(member_id):
        """ ===== QRコード生成（会員番号ベース）===== """
        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(member_id)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        qr_img = qr_img.resize((QR_SIZE, QR_SIZE))
        return qr_img

__doc__="""
Usage:
    create_ticket_image [(--key <sheet_key>)|(-K <sheet_id>)] [(--sheet-name <sheet_name>)|(-N <sheet_name>)] [(--image-template-path <image_template_path>)|(-I <image_template_path>)] [(-d <directory>)] [(--key-file <keyfile>)]
"""

def main(argv=sys.argv[1:]):
    args=docopt.docopt(__doc__,argv)

    #引数の取得
    sheet_key=args["<sheet_key>"] or DEF_SPREADSHEET_KEY
    sheet_name=args["<sheet_name>"] or DEF_SHEET_NAME
    image_template_path=args["<image_template_path>"] or DEF_IMAGE_TEMPLATE_PATH
    directory=args["<directory>"] or OUTPUT_DIR
    keyfile=args["<keyfile>"] or DEF_KEYFILE

    client=get_client(keyfile)
    ws = client.open_by_key(sheet_key).worksheet(sheet_name)
    os.makedirs(directory, exist_ok=True)

    # 1行目ヘッダ想定: 会員番号, 名前
    rows = ws.get_all_records()  # list[dict]

    #font = ImageFont.truetype("arial.ttf",size=FONT_SIZE)

    for row in rows:
        member_id = str(row["会員番号"])
        name = row["名前"]

        qr_img=create_qrcode(member_id)

        #フォーマット画像にQRコードを合成 
        image = Image.open(image_template_path).convert("RGB")
        image.paste(qr_img, QR_POS)

        #テキスト描画
        draw = ImageDraw.Draw(image)
        draw.text(NAME_POS, name,font=NAME_FONT,fill="white")
        draw.text(ID_POS, member_id,font=ID_FONT, fill="white")

        #ファイルとして保存
        out_path = os.path.join(OUTPUT_DIR, f"{member_id}_{name}.png")
        image.save(out_path)
        msg=f"saved:{out_path}"
        logger.info(msg)


if __name__ == "__main__":
     """
     パラメータ
        sheet id
        sheet name
        template path
        output directory
     """
     main()