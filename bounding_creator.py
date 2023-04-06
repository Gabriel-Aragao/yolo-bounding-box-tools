import os
import cv2

# Variáveis globais
image_files = []
current_image_index = 0
drawing = False
start_point = ()
end_point = ()
current_image = None
window_name = 'Image Bounding Box Selector'
bounding_boxes = []

def on_mouse(event, x, y, flags, param):
    global drawing, start_point, end_point, current_image

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_point = (x, y)
            image_copy = current_image.copy()
            cv2.rectangle(image_copy, start_point, end_point, (0, 255, 0), 2)
            cv2.imshow(window_name, image_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        bounding_boxes.append((start_point, end_point))
        cv2.rectangle(current_image, start_point, end_point, (0, 255, 0), 2)
        cv2.imshow(window_name, current_image)

def save_bounding_boxes(image_path, bounding_boxes, img_shape):
    annotations = []

    for start_point, end_point in bounding_boxes:
        x_min, y_min = start_point
        x_max, y_max = end_point
        x_center = (x_min + x_max) / 2
        y_center = (y_min + y_max) / 2
        width = x_max - x_min
        height = y_max - y_min

        x_center /= img_shape[1]
        y_center /= img_shape[0]
        width /= img_shape[1]
        height /= img_shape[0]

        class_id = 0  # Altere este valor para o ID de classe apropriado
        yolo_annotation = f"{class_id} {x_center} {y_center} {width} {height}"
        annotations.append(yolo_annotation)

    txt_file = image_path.replace('.jpg', '.txt')
    with open(txt_file, 'w') as f:
        f.write("\n".join(annotations))

def on_key_press(key):
    global current_image_index, start_point, end_point, current_image, bounding_boxes
    if key == ord('q'):  # Pressione 'q' para sair do programa
        return False
    elif key == ord('n'):  # Pressione 'n' para salvar o bounding box e avançar para a próxima imagem
        if bounding_boxes:
            save_bounding_boxes(image_files[current_image_index], bounding_boxes, current_image.shape)
            bounding_boxes = []
        current_image_index += 1
        if current_image_index < len(image_files):
            current_image = cv2.imread(image_files[current_image_index])
            cv2.imshow(window_name, current_image)
    elif key == ord('b'):  # Pressione 'b' para voltar à imagem anterior
        if current_image_index > 0:            
            current_image_index -= 1
            current_image = cv2.imread(image_files[current_image_index])
            cv2.imshow(window_name, current_image)
    elif key == ord('c'):  # Pressione 'c' para limpar o último bounding box
        if bounding_boxes:            
            bounding_boxes.pop()
            current_image = cv2.imread(image_files[current_image_index])
            for box in bounding_boxes:
                cv2.rectangle(current_image, box[0], box[1], (0, 255, 0), 2)
            cv2.imshow(window_name, current_image)

    return True

def main():
    global image_files, current_image_index, current_image

    directory = 'upload'
    image_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.jpg')]

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 1366, 768)
    cv2.setMouseCallback(window_name, on_mouse)

    if len(image_files) > 0:
        current_image = cv2.imread(image_files[current_image_index])

        text = "clear -> c | next -> n | back -> b"
        image_with_text = current_image.copy()

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

        keep_running = True
        while current_image_index < len(image_files) and keep_running:
            key = cv2.waitKey(1)
            if key != -1:
                keep_running = on_key_press(key)

    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
