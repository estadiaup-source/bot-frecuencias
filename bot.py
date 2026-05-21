from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# ====================================
# FIREBASE
# ====================================

cred = credentials.Certificate(
    "inventario-y-estatus-firebase-adminsdk-fbsvc-3bebc5b92a.json"
)

firebase_admin.initialize_app(cred)

db = firestore.client()

# ====================================
# TOKEN BOT
# ====================================

import os

TOKEN = os.getenv("BOT_TOKEN")
# ====================================
# ESTADOS
# ====================================

usuarios_estado = {}

# ====================================
# START
# ====================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    teclado = [

        ["Agregar Inventario"],

        ["Agregar Frecuencia"],

        ["Salir"],

    ]

    reply_markup = ReplyKeyboardMarkup(

        teclado,

        resize_keyboard=True,

    )

    await update.message.reply_text(

        "👋 Bienvenido al sistema CFE",

        reply_markup=reply_markup,

    )

# ====================================
# MENSAJES
# ====================================

async def mensajes(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    texto = update.message.text
    chat_id = update.message.chat_id

    # ====================================
    # SALIR
    # ====================================

    if texto == "Salir":

        usuarios_estado.pop(
            chat_id,
            None,
        )

        teclado = [

            ["Agregar Inventario"],

            ["Agregar Frecuencia"],

        ]

        reply_markup = ReplyKeyboardMarkup(

            teclado,

            resize_keyboard=True,

        )

        await update.message.reply_text(

            "👋 Sesión finalizada",

            reply_markup=reply_markup,

        )

        return

    # ====================================
    # INVENTARIO
    # ====================================

    if texto == "Agregar Inventario":

        usuarios_estado[chat_id] = {

            "tipo": "inventario",

            "paso": 1,

        }

        await update.message.reply_text(
            "📦 Nombre:"
        )

        return

    # ====================================
    # FRECUENCIAS
    # ====================================

    if texto == "Agregar Frecuencia":

        usuarios_estado[chat_id] = {

            "tipo": "frecuencia",

            "paso": 1,

        }

        teclado = [

            ["Zona San Cristóbal"],

            ["Zona 2"],

            ["Zona 3"],

        ]

        reply_markup = ReplyKeyboardMarkup(

            teclado,

            resize_keyboard=True,

            one_time_keyboard=True,

        )

        await update.message.reply_text(

            "📡 Selecciona zona:",

            reply_markup=reply_markup,

        )

        return

    # ====================================
    # FLUJOS
    # ====================================

    if chat_id in usuarios_estado:

        estado = usuarios_estado[chat_id]

        # ====================================
        # INVENTARIO
        # ====================================

        if estado["tipo"] == "inventario":

            if estado["paso"] == 1:

                estado["Nombre"] = texto
                estado["paso"] = 2

                await update.message.reply_text(
                    "📦 Cantidad:"
                )

                return

            elif estado["paso"] == 2:

                estado["Cantidad"] = texto
                estado["paso"] = 3

                teclado = [

                    ["Operativo"],

                    ["Dañado"],

                    ["Mantenimiento"],

                ]

                reply_markup = ReplyKeyboardMarkup(

                    teclado,

                    resize_keyboard=True,

                    one_time_keyboard=True,

                )

                await update.message.reply_text(

                    "📦 Estado:",

                    reply_markup=reply_markup,

                )

                return

            elif estado["paso"] == 3:

                estado["Estado"] = texto
                estado["paso"] = 4

                await update.message.reply_text(
                    "👤 Responsable:"
                )

                return

            elif estado["paso"] == 4:

                estado["Responsable"] = texto
                estado["paso"] = 5

                await update.message.reply_text(
                    "🛠 Último mantenimiento:"
                )

                return

            elif estado["paso"] == 5:

                estado["UltimoMantenimiento"] = texto
                estado["paso"] = 6

                await update.message.reply_text(
                    "📝 Observaciones:"
                )

                return

            elif estado["paso"] == 6:

                estado["Observaciones"] = texto

                nuevo_equipo = db.collection(
                    "equipos"
                ).document()

                nuevo_equipo.set({

                    "Nombre":
                        estado["Nombre"],

                    "Cantidad":
                        estado["Cantidad"],

                    "Estado":
                        estado["Estado"],

                    "Responsable":
                        estado["Responsable"],

                    "UltimoMantenimiento":
                        estado["UltimoMantenimiento"],

                    "Observaciones":
                        estado["Observaciones"],

                    "QR":
                        nuevo_equipo.id,

                })

                teclado = [

                    ["Agregar Inventario"],

                    ["Agregar Frecuencia"],

                    ["Salir"],

                ]

                reply_markup = ReplyKeyboardMarkup(

                    teclado,

                    resize_keyboard=True,

                )

                await update.message.reply_text(

                    "✅ Equipo agregado correctamente",

                    reply_markup=reply_markup,

                )

                del usuarios_estado[chat_id]

                return

        # ====================================
        # FRECUENCIAS
        # ====================================

        if estado["tipo"] == "frecuencia":

            if estado["paso"] == 1:

                estado["Zona"] = texto
                estado["paso"] = 2

                await update.message.reply_text(
                    "📡 Repetidor:"
                )

                return

            elif estado["paso"] == 2:

                estado["Repetidor"] = texto
                estado["paso"] = 3

                await update.message.reply_text(
                    "📡 Tipo:"
                )

                return

            elif estado["paso"] == 3:

                estado["Tipo"] = texto
                estado["paso"] = 4

                await update.message.reply_text(
                    "📡 TX:"
                )

                return

            elif estado["paso"] == 4:

                estado["TX"] = texto
                estado["paso"] = 5

                await update.message.reply_text(
                    "📡 RX:"
                )

                return

            elif estado["paso"] == 5:

                estado["RX"] = texto
                estado["paso"] = 6

                await update.message.reply_text(
                    "📡 Canal:"
                )

                return

            elif estado["paso"] == 6:

                estado["Canal"] = texto

                db.collection(
                    "frecuencias"
                ).add({

                    "Zona":
                        estado["Zona"],

                    "Repetidor":
                        estado["Repetidor"],

                    "Tipo":
                        estado["Tipo"],

                    "TX":
                        estado["TX"],

                    "RX":
                        estado["RX"],

                    "Canal":
                        estado["Canal"],

                })

                teclado = [

                    ["Agregar Inventario"],

                    ["Agregar Frecuencia"],

                    ["Salir"],

                ]

                reply_markup = ReplyKeyboardMarkup(

                    teclado,

                    resize_keyboard=True,

                )

                await update.message.reply_text(

                    "✅ Frecuencia agregada correctamente",

                    reply_markup=reply_markup,

                )

                del usuarios_estado[chat_id]

                return

# ====================================
# APP
# ====================================

app = ApplicationBuilder().token(
    TOKEN
).build()

app.add_handler(
    CommandHandler("start", start)
)

app = Application.builder().token(TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.ALL,
        manejar_mensaje,
    )
)

print("Bot activo...")

app.run_polling()