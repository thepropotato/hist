import base64

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")

# Replace 'your_image.jpg' with the path to your image file
image_path = "C://Users//venup//Desktop//images//refresh.png"
base64_string = image_to_base64(image_path)

# Write the base64 string to a text file
output_file_path = "C://Users//venup//Desktop//base64//refresh.txt"
with open(output_file_path, 'w') as output_file:
    output_file.write(base64_string)

print(f"Base64-encoded image string written to {output_file_path}")
