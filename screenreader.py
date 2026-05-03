import pytesseract
import pyautogui
import cv2
import base64
from PIL import Image
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("acessibilidade")
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

@mcp.tool()
def ler_tela_para_o_gemma() -> str:
    try:
        screenshot = pyautogui.screenshot()
        screenshot = screenshot.convert('L')
        texto = pytesseract.image_to_string(screenshot, lang='eng')
        if not texto.strip():
                return "A tela parece estar vazia ou não consegui identificar texto legível."
        
        return f"Conteúdo da tela:\n{texto}"
    except Exception as e:
        return f"Erro ao ler a tela: {str(e)}"


@mcp.tool()
def capturar_foto_webcam() -> str:
    """Captura uma imagem da webcam do notebook e tenta descrever o ambiente."""
    camera = cv2.VideoCapture(0) # 0 é a câmera padrão
    if not camera.isOpened():
        return "Erro: Não foi possível acessar a webcam."

    ret, frame = camera.read()
    if ret:
        # Salva temporariamente ou processa
        cv2.imwrite("webcam_capture.jpg", frame)
        camera.release()
        
        # Aqui você poderia integrar com um OCR ou apenas avisar ao Gemma
        return "Foto capturada com sucesso. O arquivo webcam_capture.jpg está pronto para análise."
    
    camera.release()
    return "Falha ao capturar imagem da webcam."

if __name__ == "__main__":
    mcp.run()