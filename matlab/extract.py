from PIL import Image, ImageOps

def pick_image(mat_image, n):
    img_array = mat_image[n].reshape((28, 28), order='F')
    img = Image.fromarray(img_array).convert('RGB')  # グレースケール画像化
    img = ImageOps.invert(img)
    return img

