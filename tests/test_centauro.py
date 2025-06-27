import re
from playwright.sync_api import Playwright, sync_playwright, expect

import json
with open("datos_producto_Centauro.json", "r") as file:
    data = json.load(file)

usuario = data["usuario"]
contrasena = data["contrasena"]
producto = data["producto"]


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=3000)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://csl-tst.outsystemsenterprise.com/FacturaZen/")

    page.locator("#b1-Input_Username").click()
    page.locator("#b1-Input_Username").fill(usuario)
    page.locator("#b1-Input_Password").click()
    page.locator("#b1-Input_Password").fill(contrasena)
    page.get_by_role("button", name="Inicio de sesión").click()


    page.goto("https://csl-tst.outsystemsenterprise.com/FacturaZen/Dashboard")

    page.locator("#b1-b2-b1-b3-\$b1 > div > div > span").wait_for(state="visible", timeout=15000)
       
    page.get_by_role("button", name="Productos y Servicios").click()
    page.get_by_role("button", name="Nuevo producto").click()
    page.get_by_role("textbox").click()

    page.get_by_role("textbox").fill(producto["codigo"])
    page.get_by_role("button", name="Buscar").click()
    page.get_by_role("checkbox").check()
    page.get_by_role("button", name="Siguiente").click()

    page.locator("div").filter(has_text=re.compile(r"^Medida Comercial$")).get_by_role("textbox").click()
    page.locator("div").filter(has_text=re.compile(r"^Medida Comercial$")).get_by_role("textbox").fill(producto["medida_comercial"])
    page.get_by_role("combobox").first.select_option(producto["unidad"])
    page.locator("div").filter(has_text=re.compile(r"^Precio Unitario$")).get_by_role("textbox").click()
    page.locator("div").filter(has_text=re.compile(r"^Precio Unitario$")).get_by_role("textbox").fill(producto["precio"])
    page.get_by_role("textbox").nth(3).click()
    page.get_by_role("textbox").nth(3).fill(producto["detalle"])
    page.get_by_role("button", name="Guardar").click()
    
    page.locator("div").filter(has_text=re.compile(r"^Hola MaríaNovedadesAyuda$")).get_by_role("button").click()
    
    context.close()
    browser.close() 
    


with sync_playwright() as playwright:
    run(playwright)