import os
import cv2
import numpy as np

window_name = 'Image with Bounding Boxes'

def get_files_from_directory(directory, extension):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(extension)]

def read_yolo_annotation(file_path, img_shape):
    with open(file_path, 'r') as f:
        boxes = []
        lines = f.readlines()
        for line in lines:
            data = line.strip().split()
            class_id = int(data[0])
            x, y, w, h = map(float, data[1:])
            x_min = int((x - w / 2) * img_shape[1])
            x_max = int((x + w / 2) * img_shape[1])
            y_min = int((y - h / 2) * img_shape[0])
            y_max = int((y + h / 2) * img_shape[0])
            boxes.append((class_id, x_min, y_min, x_max, y_max))
    return boxes

def draw_boxes(image, boxes, color=(0, 255, 0), thickness=2):
    for box in boxes:
        class_id, x_min, y_min, x_max, y_max = box
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, thickness)
        cv2.putText(image, str(class_id), (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    return image

def main():
    directory = 'teste'
    image_files = get_files_from_directory(directory, '.jpg')

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1366, 768)

    for image_file in image_files:
        txt_file = image_file.replace('.jpg', '.txt')
        if not os.path.exists(txt_file):
            continue

        image = cv2.imread(image_file)
        boxes = read_yolo_annotation(txt_file, image.shape)
        image_with_boxes = draw_boxes(image, boxes)


        text = "next -> press any key"
        image_with_text = image_with_boxes.copy()

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8 # Reduza o tamanho da fonte
        font_color = (0, 0, 0)
        thickness = 2
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness=thickness)
        
        # Defina as coordenadas do retângulo de fundo
        rect_x = int(image_with_text.shape[1] - text_size[0])
        rect_y = int(0)
        rect_width = int(text_size[0])
        rect_height = int(text_size[1] + 10)

        # Desenhe o retângulo de fundo na imagem
        cv2.rectangle(image_with_text, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (255, 255, 255), cv2.FILLED)

        # Posicione o texto à direita da imagem
        text_x = int(image_with_text.shape[1] - text_size[0]) # Adicione uma margem de 10 pixels
        text_y = int(text_size[1])

        # Use cv2.putText para exibir o texto
        cv2.putText(image_with_text, text, (text_x, text_y), font, font_scale, font_color, thickness=thickness, lineType=cv2.LINE_AA, bottomLeftOrigin=False)
        
        cv2.imshow(window_name, image_with_text)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
