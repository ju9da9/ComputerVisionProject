# Trabalho Prático 1 - Python | Practical Work 1 - Python

## Descrição | Description

Este projeto Python foi desenvolvido como parte do Trabalho Prático 1 da Unidade Curricular de Visão Computacional, lecionada no 2º ano do Mestrado em Engenharia Eletrotécnica, Politécnico de Leiria. O código possui funcionalidades avançadas para manipulação de vídeos, incluindo modos de vídeo e modos em escala de cinza. Além disso, há opções para definir atrasos e *frames* iniciais.  

This Python project was developed as part of Practical Work 1 of the Computer Vision course, taught in the 2nd year of the Master’s Degree in Electrical Engineering at the Polytechnic Institute of Leiria. The code includes advanced functionalities for video manipulation, including video modes and grayscale modes. Additionally, there are options to define delays and initial frames.

---

## Requisitos | Requirements

- Python 3.12.6  
- Bibliotecas necessárias | Required libraries:
    - os  
    - cv2  
    - numpy  
    - pyplot (matplotlib)  
    - math  
    - csv  
    - sys  

---

## Funcionalidades | Functionalities

- **Modo Vídeo (`video_mode`)**: Ativa o modo de vídeo para processamento (`TRUE`); (__linha 952__)  
  **Video Mode (`video_mode`)**: Enables video processing mode (`TRUE`); (__line 952__)

- **Modo Cinza (`gray_mode`)**: Converte o vídeo para escala de cinza (`TRUE`) ou para a escala de cores HSV (`FALSE`); (__linha 945__)  
  **Grayscale Mode (`gray_mode`)**: Converts video to grayscale (`TRUE`) or to HSV color space (`FALSE`); (__line 945__)

- **Atraso (`delay`)**: Define o atraso entre os quadros do vídeo (ex: `200` 🠊 200ms = 0.2s por *frame*); (__linha 1019__)  
  **Delay (`delay`)**: Defines the delay between video frames (e.g., `200` 🠊 200ms = 0.2s per frame); (__line 1019__)

- ***Frame* Inicial (`starting_frame`)**: Define o frame inicial para processamento (de `0` a `1800`). (__linha 1017__)  
  **Starting Frame (`starting_frame`)**: Defines the initial frame for processing (from `0` to `1800`). (__line 1017__)

**AVISO | WARNING**: O `video_mode` só funciona quando `gray_mode` está definido como FALSE. Se `gray_mode` estiver TRUE, o modo vídeo não estará disponível.  
`video_mode` only works when `gray_mode` is set to FALSE. If `gray_mode` is TRUE, video mode will not be available.

---

## Funções utilizadas | Functions used

- **is_point_in_circle(x, y, cx, cy, r)**: Verifica se um ponto está dentro de um círculo.  
  Checks whether a point is inside a circle.

- **agrupar_linhas(lines, pos_cir_x, pos_cir_y, raio, angle_threshold=12, proximity_threshold=20)**: Agrupa linhas próximas e quase paralelas.  
  Groups nearby and almost parallel lines.

- **distance_between_parallel_lines(line1, line2)**: Calcula a distância entre duas linhas paralelas.  
  Computes distance between two parallel lines.

- **detetar_ponteiros(grupos, pos_cir_x, pos_cir_y, ponteiro_segundos)**: Deteta os ponteiros do relógio.  
  Detects clock hands.

- **get_hands(hands)**: Determina ponteiros de hora, minuto e segundo.  
  Determines hour, minute, and second hands.

- **get_hands_V(hands, second_hand)**: Determina ponteiros de hora e minuto.  
  Determines hour and minute hands.

- **get_hands_S(hands)**: Determina o ponteiro dos segundos.  
  Determines the second hand.

- **calculate_rect_coordinates(line)**: Calcula coordenadas de um retângulo.  
  Calculates rectangle coordinates around a line.

- **draw_ponteiros_frame(img, hour_hand, minute_hand, second_hand)**: Desenha ponteiros na imagem.  
  Draws clock hands on the image.

- **get_vector(hand)**: Calcula vetor direcional de um ponteiro.  
  Computes directional vector of a hand.

- **dot_product(u, v)**: Produto escalar de vetores.  
  Dot product of vectors.

- **cross_product(u, v)**: Produto vetorial de vetores.  
  Cross product of vectors.

- **get_angle(hand, center_x, center_y)**: Calcula ângulo do ponteiro.  
  Computes hand angle.

- **get_time(hour_angle, minute_angle, second_angle)**: Calcula o tempo.  
  Computes time from angles.

- **draw_time(img, time)**: Desenha o tempo na imagem.  
  Draws time on image.

- **detect_region_of_interest(detect_circles, image, gray_mode, video_mode)**: Deteta região de interesse.  
  Detects region of interest.

- **detect_ponteiros(image, S_image, V_image, masked_image, pos_cir_x, pos_cir_y, raio_cir, gray_mode, video_mode)**: Deteta ponteiros do relógio.  
  Detects clock hands in image.

- **main()**: Função principal do programa.  
  Main program function.

---

## Contato | Contact

📧 [juda.imbo99@gmail.com](mailto:juda.imbo99@gmail.com)
