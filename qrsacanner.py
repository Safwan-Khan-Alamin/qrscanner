import qrcode
import os
import io
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import win32clipboard

def send_to_clipboard(img: Image.Image):
    output = io.BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

# Create output folder
output_folder = "qrcodes"
os.makedirs(output_folder, exist_ok=True)

print("Hello! This is Safwan Khan Al-amin.")
print("Please enter your link or text to create your QR code.")
print("Type 'exit' to stop the program.\n")

while True:
    data = input("Enter Your Link:\n")
    
    if data.lower() == "exit":
        print("👋 Exiting... Thank you!")
        break
    if not data.strip():
        print("⚠️ Empty input! Please enter valid text or link.")
        continue

    # Generate QR
    qr = qrcode.QRCode(
        version=1,
        box_size=2,
        border=2
    )
    qr.add_data(data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qr_img = qr_img.resize((92, 92), Image.Resampling.LANCZOS)

    # Create canvas with background
    canvas_width = 92
    canvas_height = 110
    bg_color = (255, 230, 200)
    canvas = Image.new("RGB", (canvas_width, canvas_height), color=bg_color)
    canvas.paste(qr_img, (0, 0))

    # Add text
    draw = ImageDraw.Draw(canvas)
    font_size = 10
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    text = "SK Al-amin"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (canvas_width - text_width) // 2
    text_y = 94
    draw.text((text_x, text_y), text, fill="black", font=font)

    # Create filename
    timestamp = datetime.now().strftime("%d-%m-%y_(%I-%M-%S_%p)")
    filename = f"qr_{timestamp}.png"
    filepath = os.path.join(output_folder, filename)

    # Save and copy to clipboard
    canvas.save(filepath)
    send_to_clipboard(canvas)

    print(f"✅ QR code saved as: {filepath}")
    print("✅ QR code copied to clipboard!\n")
