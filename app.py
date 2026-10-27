import io
import os
import requests
from PIL import Image


def procesar_y_guardar_jpeg(img_pil, ruta_salida):
    """
    Gestiona el canal alfa y guarda la imagen con máxima fidelidad visual.
    """
    # Si la imagen tiene transparencia, la colocamos sobre un fondo blanco
    if img_pil.mode in ("RGBA", "LA") or (img_pil.mode == "P" and "transparency" in img_pil.info):
        img_rgba = img_pil.convert("RGBA")
        fondo_blanco = Image.new("RGB", img_rgba.size, (255, 255, 255))
        fondo_blanco.paste(img_rgba, mask=img_rgba.split()[3])
        imagen_final = fondo_blanco
    else:
        imagen_final = img_pil.convert("RGB")

    # Guardado con máxima calidad
    imagen_final.save(
        ruta_salida,
        "JPEG",
        quality=100,
        subsampling=0,
        keep_rgb=True
    )
    print(f"\n✅ ¡Éxito! Imagen guardada en: {ruta_salida}")


def convertir_archivo_local():
    """
    Lista los archivos .webp del espacio de trabajo actual o permite escribir una ruta.
    """
    extensiones = (".webp", ".WEBP")
    archivos = [f for f in os.listdir(".") if f.endswith(extensiones)]

    ruta_archivo = ""

    if archivos:
        print("\nImágenes WEBP encontradas en la carpeta actual:")
        for idx, archivo in enumerate(archivos, 1):
            print(f"  [{idx}] {archivo}")
        print("  [0] Escribir otra ruta manualmente")

        seleccion = input("\nElige el número de la imagen o escribe la ruta: ").strip()

        if seleccion.isdigit():
            num = int(seleccion)
            if 1 <= num <= len(archivos):
                ruta_archivo = archivos[num - 1]
            elif num == 0:
                ruta_archivo = input("Escribe la ruta completa o relativa del archivo: ").strip()
            else:
                print("Número fuera de rango.")
                return
        else:
            ruta_archivo = seleccion
    else:
        ruta_archivo = input("\nNo hay archivos .webp en la raíz. Escribe la ruta del archivo: ").strip()

    if not ruta_archivo or not os.path.exists(ruta_archivo):
        print(f"❌ Error: El archivo '{ruta_archivo}' no existe.")
        return

    nombre_base = os.path.splitext(ruta_archivo)[0]
    ruta_salida = f"{nombre_base}.jpg"

    try:
        with Image.open(ruta_archivo) as img:
            procesar_y_guardar_jpeg(img, ruta_salida)
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")


def convertir_desde_url():
    """
    Descarga una imagen WEBP desde un enlace y la convierte a JPEG.
    """
    url = input("\nPega la URL de la imagen WEBP: ").strip()

    if not url:
        print("Operación cancelada: URL vacía.")
        return

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        print("⏳ Descargando imagen...")
        respuesta = requests.get(url, headers=headers, timeout=15)
        respuesta.raise_for_status()

        buffer_imagen = io.BytesIO(respuesta.content)

        with Image.open(buffer_imagen) as img:
            nombre_sugerido = url.split("?")[0].split("/")[-1]
            nombre_base = os.path.splitext(nombre_sugerido)[0] or "imagen_descargada"
            ruta_salida = f"{nombre_base}.jpg"

            procesar_y_guardar_jpeg(img, ruta_salida)

    except requests.exceptions.RequestException as e:
        print(f"❌ Error de red/descarga: {e}")
    except Exception as e:
        print(f"❌ Error al procesar la imagen: {e}")


def menu_principal():
    while True:
        print("\n" + "=" * 45)
        print(" CONVERSOR WEBP A JPEG (CALIDAD MÁXIMA)")
        print("=" * 45)
        print("1. Elegir archivo local en el Codespace")
        print("2. Descargar y convertir desde una URL")
        print("3. Salir")

        opcion = input("\nElige una opción (1-3): ").strip()

        if opcion == "1":
            convertir_archivo_local()
        elif opcion == "2":
            convertir_desde_url()
        elif opcion == "3":
            print("\nSaliendo...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu_principal()