# bot.py (versão com logging e tratamento de erros)
import os
import glob
import time
import traceback
import telebot
from telebot import types

TOKEN = "8596940933:AAG9qQ0xWxZ8AdnEFxMh7Xd6WA8P2Mhdd8Q"
bot = telebot.TeleBot(TOKEN)

# --- Utils de logging ---
def log_exception(exc: Exception):
    tb = traceback.format_exc()
    print(tb)
    try:
        with open("errors.log", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - ERROR\n")
            f.write(tb + "\n\n")
    except Exception as e:
        print("Falha ao gravar errors.log:", e)

# --- procura video ---
def find_video_file():
    patterns = ["video.mp4", "video.mov", "video.MP4", "video.MOV", "video.*"]
    for p in patterns:
        matches = glob.glob(p)
        if matches:
            return matches[0]
    for ext in ("*.mp4", "*.mov", "*.mkv", "*.webm"):
        m = glob.glob(ext)
        if m:
            return m[0]
    return None

# --- envio seguro de vídeo ---
def safe_send_video(chat_id):
    try:
        vf = find_video_file()
        if vf:
            with open(vf, "rb") as f:
                bot.send_video(chat_id, f, caption="💗 Oi amor, olha isso antes de tudo 💗")
                time.sleep(0.3)
        else:
            bot.send_message(chat_id, "(Sem vídeo) Coloque video.mp4 ou video.mov na pasta do bot.")
            time.sleep(0.2)
    except Exception as e:
        log_exception(e)
        bot.send_message(chat_id, "❌ Erro ao enviar o vídeo. Contate o suporte.")
        time.sleep(0.2)

# --- menus ---
def menu_inicial(chat_id):
    try:
        safe_send_video(chat_id)

        texto = (
            "Oiee amor, como você está? Seja bem-vindo! 🤩\n\n"
            "O que te espera no meu VIP? 🤭\n\n"
            "💗 Vídeos e fotos novinhos TODO DIA\n"
            "💗 Exibicionismo sem vergonha nenhuma\n"
            "💗 Brinquedinhos bem enfiadinhos…\n"
            "💗 Masturbação lenta e bem provocante\n"
            "💗 Masturbação anal de deixar você babando\n"
            "💗 Chamadinhas de vídeo AO VIVO só pra você 😏\n\n"
            "✨ Mais de 500 conteúdos + atualizações diárias 🔥\n"
            "🔐 Compra 100% segura — sigilo total\n\n"
            "Vem me ver todinha… todos os dias 😘👇🏼"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💖 Garantir Acesso 💖", callback_data="acesso"))
        markup.add(types.InlineKeyboardButton("✨ Ver Prévias ✨", callback_data="previas"))

        bot.send_message(chat_id, texto, reply_markup=markup)
        time.sleep(0.2)
    except Exception as e:
        log_exception(e)
        bot.send_message(chat_id, "❌ Erro no menu inicial.")

def menu_planos(chat_id):
    try:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💗 VIP SEMANAL + MIMO — R$ 13,87", callback_data="plano_semanal"))
        markup.add(types.InlineKeyboardButton("💗 VIP MENSAL + BRINDES — R$ 19,91", callback_data="plano_mensal"))
        markup.add(types.InlineKeyboardButton("💗 VITALÍCIO + WHATSAPP — R$ 49,97", callback_data="plano_vitalicio"))
        bot.send_message(chat_id, "Escolha seu plano, amor 😘👇🏼", reply_markup=markup)
        time.sleep(0.2)
    except Exception as e:
        log_exception(e)
        bot.send_message(chat_id, "❌ Erro ao mostrar planos.")

def tela_pagamento(chat_id, plano_label):
    try:
        pix_fake = "000201000000000000000000000000000000000000000000000000000000"

        mensagens = [
            "💗 Carol Beatriz:\nAguarde um momento enquanto preparamos tudo :)",
            "💗 Carol Beatriz:\nPara efetuar o pagamento, utiliza a opção \"Pagar > PIX copia e Cola\" no aplicativo do seu banco.",
            "💗 Carol Beatriz:\nCopie o código abaixo:",
            f"💗 Carol Beatriz:\n`{pix_fake}`",
            "💗 Carol Beatriz:\nApós efetuar o pagamento, clique no botão abaixo ⤵️"
        ]

        for m in mensagens:
            try:
                bot.send_message(chat_id, m, parse_mode="Markdown")
            except Exception:
                bot.send_message(chat_id, m)
            time.sleep(0.25)

        teclado = types.InlineKeyboardMarkup()
        teclado.add(types.InlineKeyboardButton("✅ Já paguei!", callback_data="finalizar"))
        bot.send_message(chat_id, " ", reply_markup=teclado)
        time.sleep(0.2)

    except Exception as e:
        log_exception(e)
        # REMOVEU A LINHA ABAIXO ↓↓↓
        # bot.send_message(chat_id, "❌ Erro ao gerar tela de pagamento.")
        pass

def finalizar_pagamento(chat_id):
    try:
        bot.send_message(chat_id, "💗 Pagamento enviado para análise! Aguarde alguns instantes 💗")
        time.sleep(0.2)
    except Exception as e:
        log_exception(e)

# --- handlers com proteção ---
@bot.message_handler(commands=["start"])
def handle_start(message):
    try:
        menu_inicial(message.chat.id)
    except Exception as e:
        log_exception(e)
        bot.send_message(message.chat.id, "❌ Ocorreu um erro ao processar /start")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass

        cid = call.message.chat.id
        data = call.data

        if data == "acesso":
            menu_planos(cid)
        elif data == "previas":
            bot.send_message(cid, "👀 Prévia: Em breve adicionaremos prévias automáticas aqui!")
        elif data == "plano_semanal":
            tela_pagamento(cid, "semanal")
        elif data == "plano_mensal":
            tela_pagamento(cid, "mensal")
        elif data == "plano_vitalicio":
            tela_pagamento(cid, "vitalicio")
        elif data == "finalizar":
            finalizar_pagamento(cid)
        else:
            bot.send_message(cid, "Opção desconhecida.")
    except Exception as e:
        log_exception(e)
        try:
            bot.send_message(call.message.chat.id, "❌ Ocorreu um erro ao processar sua ação.")
        except Exception:
            pass

# --- main ---
if __name__ == "__main__":
    print("Bot iniciado...")
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as main_exc:
        log_exception(main_exc)
        print("Erro crítico. Veja errors.log.")
