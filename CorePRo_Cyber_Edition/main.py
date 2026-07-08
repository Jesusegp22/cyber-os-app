import flet as ft
import sqlite3
import urllib.parse
from datetime import datetime, timedelta

# --- 1. MOTOR DE BASE DE DATOS LOCAL (CON ALERTA DE SEMÁFORO) ---
def inicializar_bd():
    conexion = sqlite3.connect("cyber_os_crm.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_crm (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            perfil_profesional TEXT,
            nombres TEXT,
            apellidos TEXT,
            telefono TEXT,
            correo TEXT,
            profesion_cliente TEXT,
            detalles TEXT,
            campo_mutante1 TEXT,
            campo_mutante2 TEXT,
            campo_mutante3 TEXT,
            saldo_pendiente REAL,
            dropdown_mutante TEXT,
            fecha_registro TEXT,
            fecha_vencimiento TEXT,
            estado_semaforo TEXT
        )
    """)
    conexion.commit()
    conexion.close()

def guardar_registro_bd(datos):
    conexion = sqlite3.connect("cyber_os_crm.db")
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO registros_crm (
            perfil_profesional, nombres, apellidos, telefono, correo, profesion_cliente,
            detalles, campo_mutante1, campo_mutante2, campo_mutante3, saldo_pendiente,
            dropdown_mutante, fecha_registro, fecha_vencimiento, estado_semaforo
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, datos)
    conexion.commit()
    conexion.close()

# --- 2. INTERFAZ GRÁFICA PRINCIPAL ---
def main(page: ft.Page):
    page.title = "CorePro // Cyber-OS MASTER CONSOLE"
    page.theme_mode = ft.ThemeMode.DARK
    
    inicializar_bd()

    TELEFONO = "51918442529"
    USER_TELEGRAM = "JesusGomez_Soporte"
    
    msj_b2b = "Hola Jesús, vi tu aplicación en Play Store. Me interesa una personalización corporativa con servidor en la nube para mi empresa."
    msj_ind = "Hola Jesús, me interesa adquirir un Pack de Temas VIP o una personalización exclusiva para mi perfil profesional."

    # REPARADO DE RAÍZ: Direcciones nativas directas para saltar el fallo DNS_PROBE_FINISHED_NXDOMAIN
    url_ws_b2b = f"https://whatsapp.com/{TELEFONO}&text={urllib.parse.quote(msj_b2b)}"
    url_ws_ind = f"https://whatsapp.com/{TELEFONO}&text={urllib.parse.quote(msj_ind)}"
    url_tg_b2b = f"https://t.me/{USER_TELEGRAM}"

    # --- 3. DICCIONARIO MAESTRO EXPANDIDO CON CONTROL DE CONTRASTE ---
    CONFIG_PROFESIONES = {
        "MY PERSONAL (Cyberpunk / Soporte Técnico)": {
            "bg": "#06030f", "primary": "#00f0ff", "card": "#0a0515", "text": "white", "subtext": "gray",
            "titulo_form": "REGISTRO DE CLIENTES & LICENCIAS",
            "lbl_campo1": "Trabajo (Ej: Repotenciación Hardware)",
            "lbl_campo2": "Costo Total S/.",
            "lbl_campo3": "Monto Pagado S/.",
            "options_dropdown": ["Trimestral (3 meses)", "Semestral (6 meses)", "Anual / Prime (12 meses)"],
            "lbl_dropdown": "Plan de Alerta de Licencia",
            "dias_vencimiento": 90,
            "subtitulo": "EDICIÓN VIP: HUMANOIDE INTRÍNSECO"
        },
        "VIP: BIOMÉDICAS PNP (Blanco Clínico)": {
            "bg": "#f4f6f9", "primary": "#0f172a", "card": "#ffffff", "text": "#0f172a", "subtext": "#475569",
            "titulo_form": "SISTEMA DE CONTROL BIOMÉDICO - HOSPITAL PNP",
            "lbl_campo1": "Código de Equipo / CIP Personal",
            "lbl_campo2": "Presupuesto Mantenimiento S/.",
            "lbl_campo3": "Inversión Ejecutada S/.",
            "options_dropdown": ["Revisión Semanal", "Calibración Mensual", "Certificación Anual"],
            "lbl_dropdown": "Ciclo de Control Técnico",
            "dias_vencimiento": 30,
            "subtitulo": "NÚCLEO REGISTRAL BIOMÉDICO - SANIDAD POLICÍA"
        },
        "VIP: INGENIERÍA CIVIL / ARQUITECTURA": {
            "bg": "#1a0f05", "primary": "#f97316", "card": "#2e190b", "text": "white", "subtext": "gray",
            "titulo_form": "CONTROL DE OBRAS, COSTOS & PLANOS",
            "lbl_campo1": "Código de Expediente / Obra",
            "lbl_campo2": "Presupuesto Asignado S/.",
            "lbl_campo3": "Monto Valorizado S/.",
            "options_dropdown": ["Fase 1: Movimiento Tierras", "Fase 2: Estructuras", "Fase 3: Acabados / Entrega"],
            "lbl_dropdown": "Etapa de Desarrollo de Obra",
            "dias_vencimiento": 120,
            "subtitulo": "PANEL TÉCNICO DE INGENIERÍA CIVIL"
        },
        "VIP: ENFERMERÍA (Gestión de Guardias)": {
            "bg": "#041a1a", "primary": "#00f5d4", "card": "#0b2e2e", "text": "white", "subtext": "gray",
            "titulo_form": "CONTROL DE PACIENTES & GUARDIAS",
            "lbl_campo1": "Tratamiento / Inyectable Aplicado",
            "lbl_campo2": "Número de Cama / Piso",
            "lbl_campo3": "Pago por Turno S/.",
            "options_dropdown": ["Guardia Diurna (12h)", "Guardia Nocturna (12h)", "Turno Completo (24h)"],
            "lbl_dropdown": "Tipo de Jornada Realizada",
            "dias_vencimiento": 1,
            "subtitulo": "NÚCLEO SANITARIO ACTIVO"
        },
        "VIP: DERECHO / LEYES": {
            "bg": "#0a1128", "primary": "#d4af37", "card": "#1c2541", "text": "white", "subtext": "gray",
            "titulo_form": "CONTROL DE CASOS & LITIGIOS",
            "lbl_campo1": "Número de Expediente / Juzgado",
            "lbl_campo2": "Honorarios Totales S/.",
            "lbl_campo3": "Adelanto Recibido S/.",
            "options_dropdown": ["Etapa Postulatoria", "Etapa Probatoria", "Sentencia / Apelación"],
            "lbl_dropdown": "Estado del Proceso Judicial",
            "dias_vencimiento": 60,
            "subtitulo": "NÚCLEO JURÍDICO PRO"
        }
    }
    
    perfil_actual = "MY PERSONAL (Cyberpunk / Soporte Técnico)"
    conf = CONFIG_PROFESIONES[perfil_actual]

    # --- 4. CAMPOS DEL FORMULARIO CON ESTILOS AJUSTABLES ---
    txt_nombres = ft.TextField(label="Nombres", width=210)
    txt_apellidos = ft.TextField(label="Apellidos", width=210)
    txt_telefono = ft.TextField(label="Número de Teléfono", width=210)
    txt_correo = ft.TextField(label="Correo Electrónico", width=210)
    txt_profesion_cliente = ft.TextField(label="Profesión / Ocupación", width=210)
    txt_detalles = ft.TextField(label="Detalles / Cómo lo conoció", width=210)
    
    lbl_titulo_dinamico = ft.Text(conf["titulo_form"], size=16, weight="bold")
    txt_mutante1 = ft.TextField(label=conf["lbl_campo1"], width=210)
    txt_mutante2 = ft.TextField(label=conf["lbl_campo2"], width=210)
    txt_mutante3 = ft.TextField(label=conf["lbl_campo3"], width=210)
    
    container_semaforo = ft.Container(
        content=ft.Text("Selecciona una opción para calcular la visita...", color="white", size=12, text_align=ft.TextAlign.CENTER),
        padding=10,
        border_radius=10,
        bgcolor="#141124",
        width=440
    )
    
    txt_status_bd = ft.Text("", color="green", size=13, weight="bold")

    # --- 5. ALARMAS DE SEMÁFORO EN TIEMPO REAL ---
    def calcular_alerta_tiempo(e):
        if not dropdown_mutante.value:
            return
            
        fecha_actual = datetime.now()
        dias = conf["dias_vencimiento"]
        
        if "Semestral" in dropdown_mutante.value or "Mensual" in dropdown_mutante.value or "Calibración" in dropdown_mutante.value:
            dias = 180 if "Semestral" in dropdown_mutante.value else 30
        elif "Anual" in dropdown_mutante.value or "Certificación" in dropdown_mutante.value:
            dias = 365
        elif "Trimestral" in dropdown_mutante.value or "Fase 2" in dropdown_mutante.value:
            dias = 90

        fecha_fin = fecha_actual + timedelta(days=dias)
        meses_es = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Set", "Oct", "Nov", "Dic"]
        fecha_humanizada = f"{fecha_fin.day} de {meses_es[fecha_fin.month - 1]} del {fecha_fin.year}"

        if dias <= 2:
            color_alerta = "#ff0055"
            texto_semaforo = f"🔴 CRÍTICO: Planificar atención inmediata para el {fecha_humanizada}"
        elif dias <= 30:
            color_alerta = "#ffb703"
            texto_semaforo = f"🟡 ALERTA INTERMEDIA: Próxima visita agendada el {fecha_humanizada}"
        else:
            color_alerta = "#00f0ff" if conf["bg"] != "#f4f6f9" else "#00a8ff"
            texto_semaforo = f"🟢 SISTEMA ESTABLE: Próximo control establecido el {fecha_humanizada}"

        container_semaforo.bgcolor = color_alerta
        container_semaforo.content = ft.Text(texto_semaforo, color="black" if color_alerta != "#ff0055" else "white", weight="bold", size=12, text_align=ft.TextAlign.CENTER)
        page.update()

    dropdown_mutante = ft.Dropdown(
        label=conf["lbl_dropdown"],
        width=210,
        options=[ft.dropdown.Option(opt) for opt in conf["options_dropdown"]]
    )
    dropdown_mutante.on_change = calcular_alerta_tiempo

    def aplicar_estilos_contraste_campos():
        color_letra = "#0f172a" if conf["bg"] == "#f4f6f9" else "white"
        color_borde = conf["primary"]
        
        lista_campos = [txt_nombres, txt_apellidos, txt_telefono, txt_correo, txt_profesion_cliente, txt_detalles, txt_mutante1, txt_mutante2, txt_mutante3, dropdown_mutante]
        for campo in lista_campos:
            campo.color = color_letra
            campo.border_color = color_borde
            campo.label_style = ft.TextStyle(color=color_letra)

    def cambiar_sistema_operativo(nombre_perfil):
        nonlocal perfil_actual, conf
        perfil_actual = nombre_perfil
        conf = CONFIG_PROFESIONES[nombre_perfil]
        
        lbl_titulo_dinamico.value = conf["titulo_form"]
        lbl_titulo_dinamico.color = conf["primary"]
        txt_mutante1.label = conf["lbl_campo1"]
        txt_mutante2.label = conf["lbl_campo2"]
        txt_mutante3.label = conf["lbl_campo3"]
        
        dropdown_mutante.label = conf["lbl_dropdown"]
        dropdown_mutante.options = [ft.dropdown.Option(opt) for opt in conf["options_dropdown"]]
        dropdown_mutante.on_change = calcular_alerta_tiempo
        container_semaforo.bgcolor = "#141124"
        container_semaforo.content = ft.Text("Selecciona una opción para calcular la visita...", color="white", text_align=ft.TextAlign.CENTER)
        aplicar_estilos_contraste_campos()
        ir_a_mainframe()

    def procesar_y_guardar(e):
        fecha_actual = datetime.now()
        fecha_inicio_str = fecha_actual.strftime("%Y-%m-%d")
        dias = conf["dias_vencimiento"]
        if dropdown_mutante.value:
            if "Semestral" in dropdown_mutante.value or "Mensual" in dropdown_mutante.value or "Calibración" in dropdown_mutante.value:
                dias = 180 if "Semestral" in dropdown_mutante.value else 30
            elif "Anual" in dropdown_mutante.value or "Certificación" in dropdown_mutante.value:
                dias = 365
            elif "Trimestral" in dropdown_mutante.value or "Fase 2" in dropdown_mutante.value:
                dias = 90
        fecha_fin_str = (fecha_actual + timedelta(days=dias)).strftime("%Y-%m-%d")
        estado_semaforo = "VERDE" if dias > 30 else ("AMARILLO" if dias > 2 else "ROJO")
        
        costo_total = float(txt_mutante2.value or 0)
        monto_pagado = float(txt_mutante3.value or 0)
        saldo_pendiente = costo_total - monto_pagado
        
        paquete_datos = (
            perfil_actual, txt_nombres.value, txt_apellidos.value, txt_telefono.value,
            txt_correo.value, txt_profesion_cliente.value, txt_detalles.value,
            txt_mutante1.value, str(costo_total), str(monto_pagado), saldo_pendiente,
            dropdown_mutante.value, fecha_inicio_str, fecha_fin_str, estado_semaforo
        )
        guardar_registro_bd(paquete_datos)
        txt_status_bd.value = f"¡Registrado con éxito! Control establecido: {estado_semaforo}"
        
        txt_nombres.value = txt_apellidos.value = txt_telefono.value = ""
        txt_correo.value = txt_profesion_cliente.value = txt_detalles.value = ""
        txt_mutante1.value = txt_mutante2.value = txt_mutante3.value = ""
        dropdown_mutante.value = None
        container_semaforo.bgcolor = "#141124"
        container_semaforo.content = ft.Text("Selecciona una opción para calcular la visita...", color="white", text_align=ft.TextAlign.CENTER)
        page.update()

    def ir_a_mainframe(e=None):
        page.views.clear()
        page.views.append(crear_vista_mainframe())
        page.update()

    def ir_a_registro(e=None):
        page.views.clear()
        page.views.append(crear_vista_registro())
        page.update()

    def ir_a_contacto(e=None):
        page.views.clear()
        page.views.append(crear_vista_contacto_b2b())
        page.update()

    async def abrir_enlace_b2b_ws(e):
        await page.launch_url(url_ws_b2b)

    async def abrir_enlace_b2b_tg(e):
        await page.launch_url(url_tg_b2b)

    # --- 6. FUNCIÓN DE CONSTRUCCIÓN MAESTRA PARA BOTONES PERFECTAMENTE CENTRADOS ---
    def crear_boton_centrado(texto, color_fondo, color_texto, ancho, funcion_click):
        return ft.Container(
            content=ft.Text(texto, color=color_texto, weight="bold", size=12, text_align=ft.TextAlign.CENTER),
            bgcolor=color_fondo,
            width=ancho,
            height=46,
            border_radius=23,
            alignment=ft.Alignment(0, 0),
            on_click=funcion_click,
            padding=ft.Padding.symmetric(horizontal=10)
        )

    # --- 8. GENERACIÓN DE PANTALLAS GRÁFICAS ---
    def crear_vista_mainframe():
        color_escritura_botones = "black" if conf["primary"] != "#041a1a" and conf["primary"] != "#0f172a" else "white"
        return ft.View(
            route="/",
            appbar=ft.AppBar(
                title=ft.Text("COREPRO // CYBER-OS 2026", size=16, weight="bold", color=conf["primary"] if conf["bg"] != "#f4f6f9" else "#ffffff"),
                bgcolor="#0d061a" if perfil_actual == "MY PERSONAL (Cyberpunk / Soporte Técnico)" else ("#0f172a" if conf["bg"] == "#f4f6f9" else conf["card"]),
                center_title=False,
                actions=[
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(content=ft.Text("Módulo Técnico (Jesús Gómez)"), on_click=lambda _: cambiar_sistema_operativo("MY PERSONAL (Cyberpunk / Soporte Técnico)")),
                            ft.PopupMenuItem(content=ft.Text("Carrera: Biomédicas PNP"), on_click=lambda _: cambiar_sistema_operativo("VIP: BIOMÉDICAS PNP (Blanco Clínico)")),
                            ft.PopupMenuItem(content=ft.Text("Carrera: Ingeniería Civil / Arq."), on_click=lambda _: cambiar_sistema_operativo("VIP: INGENIERÍA CIVIL / ARQUITECTURA")),
                            ft.PopupMenuItem(content=ft.Text("Carrera: Enfermería"), on_click=lambda _: cambiar_sistema_operativo("VIP: ENFERMERÍA (Gestión de Guardias)")),
                            ft.PopupMenuItem(content=ft.Text("Carrera: Derecho / Leyes"), on_click=lambda _: cambiar_sistema_operativo("VIP: DERECHO / LEYES")),
                        ],
                        icon=ft.Icons.WORK_OUTLINE,
                        tooltip="MÓDULO DE CARRERAS PRO"
                    )
                ]
            ),
            controls=[
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("MASTER CONSOLE", size=22, weight="bold", color=conf["primary"] if conf["bg"] != "#f4f6f9" else "#0f172a"),
                            ft.Text(conf["subtitulo"], size=12, color=conf["subtext"]),
                            ft.Divider(color=conf["primary"], height=10),
                            ft.Container(
                                content=ft.Image(src="a.png", width=250, height=250, fit="contain"),
                                border=ft.Border.all(2, conf["primary"]),
                                border_radius=15,
                                bgcolor="#0d061a" if perfil_actual == "MY PERSONAL (Cyberpunk / Soporte Técnico)" else "#f8fafc",
                                padding=10
                            ),
                            ft.Container(
                                content=ft.Text("[LATENCIA: 0.02 MS] [HARDWARE KERNEL OPTIMIZATION]", size=11, color=conf["primary"] if conf["bg"] != "#f4f6f9" else "#ffffff", font_family="Monospace"),
                                padding=8,
                                border=ft.Border.all(1, conf["primary"]),
                                bgcolor="#0a0515" if perfil_actual == "MY PERSONAL (Cyberpunk / Soporte Técnico)" else "#0f172a"
                            ),
                            ft.Divider(color=conf["primary"], height=15),
                            ft.Row([
                                crear_boton_centrado("REGISTROS BD", conf["primary"], color_escritura_botones, 190, ir_a_registro),
                                crear_boton_centrado("COTIZAR SOFTWARE A MEDIDA", conf["primary"], color_escritura_botones, 225, ir_a_contacto)
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        border=ft.Border.all(3, conf["primary"]),
                        border_radius=25,
                        padding=20,
                        bgcolor=conf["card"],
                        width=460
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            bgcolor=conf["bg"]
        )

    def crear_vista_registro():
        color_escritura_botones = "black" if conf["primary"] != "#041a1a" and conf["primary"] != "#0f172a" else "white"
        return ft.View(
            route="/registro",
            controls=[
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("MÓDULO OPERATIVO DE BASE DE DATOS", size=18, weight="bold", color=conf["primary"]),
                            ft.Text(f"Perfil Activo: {perfil_actual}", size=12, color=conf["subtext"]),
                            ft.Divider(color=conf["primary"], height=10),
                            ft.Text("Identificación del Contacto / Sujeto", color=conf["text"], weight="bold", size=13),
                            ft.Row([txt_nombres, txt_apellidos], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([txt_telefono, txt_correo], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([txt_profesion_cliente, txt_detalles], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Divider(color=conf["primary"], height=10),
                            lbl_titulo_dinamico,
                            ft.Row([txt_mutante1, dropdown_mutante], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([txt_mutante2, txt_mutante3], alignment=ft.MainAxisAlignment.CENTER),
                            container_semaforo,
                            ft.Divider(color=conf["primary"], height=15),
                            txt_status_bd,
                            ft.Row([
                                crear_boton_centrado("REGISTRAR EN SQLITE", conf["primary"], color_escritura_botones, 200, procesar_y_guardar),
                                crear_boton_centrado("VOLVER AL MENÚ", conf["primary"], color_escritura_botones, 200, ir_a_mainframe)
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        border=ft.Border.all(3, conf["primary"]),
                        border_radius=25,
                        padding=20,
                        bgcolor=conf["card"],
                        width=490
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            bgcolor=conf["bg"]
        )

    def crear_vista_contacto_b2b():
        return ft.View(
            route="/contacto",
            controls=[
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("SOLUCIONES CORPORATIVAS B2B", size=18, weight="bold", color="#00f0ff"),
                            ft.Text("SERVICIOS DE PERSONALIZACIÓN EXCLUSIVA", size=12, color="white"),
                            ft.Divider(color="#00f0ff", height=10),
                            ft.Container(
                                content=ft.Image(src="a.png", width=150, height=150, fit="contain"),
                                border=ft.Border.all(2, "#bc00dd"),
                                border_radius=15,
                                bgcolor="#0d061a",
                                padding=5
                            ),
                            ft.Text(
                                "¿Deseas adaptar este sistema CorePro con el logotipo de tu empresa, "
                                "colores corporativos de tu marca y base de datos centralizada en red "
                                "sincronizada en tiempo real entre tus dispositivos tecnológicos de trabajo?",
                                text_align=ft.TextAlign.CENTER, color="white", size=12
                            ),
                            ft.Divider(color="#00f0ff", height=10),
                            ft.Text("COMUNÍCATE A LAS REDES DE LA EMPRESA:", size=11, weight="bold", color="#00f0ff"),
                            ft.Row([
                                crear_boton_centrado("WHATSAPP EMPRESA", "#25D366", "white", 195, abrir_enlace_b2b_ws),
                                crear_boton_centrado("TELEGRAM SERVIDORES", "#0088cc", "white", 195, abrir_enlace_b2b_tg)
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                            ft.Divider(color="#00f0ff", height=10),
                            crear_boton_centrado("REGRESAR AL MENU", "#1a1a2e", "#00f0ff", 210, ir_a_mainframe)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        border=ft.Border.all(3, "#00f0ff"),
                        border_radius=25,
                        padding=20,
                        bgcolor="#0a0515",
                        width=460
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            bgcolor="#06030f"
        )

    # Inyección limpia del ciclo de arranque
    aplicar_estilos_contraste_campos()
    page.views.append(crear_vista_mainframe())
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
