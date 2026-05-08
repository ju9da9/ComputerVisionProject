# Trabalho Prático 1 - Python

## Descrição

Este projeto Python foi desenvolvido como parte do Trabalho Prático 1 da Unidade Curricular de Visão Computacional, lecionada no 2º ano do Mestrado em Engenharia Eletrotécnica, Politécnico de Leiria. O código possui funcionalidades avançadas para manipulação de vídeos, incluindo modos de vídeo e modos em escala de cinza. Além disso, há opções para definir atrasos e *frames* iniciais.


## Requisitos

- Python 3.12.6
- Bibliotecas necessárias:
    - os
    - cv2 
    - numpy
    - pyplot (matplotlib)
    - math
    - os
    - csv
    - sys


## Funcionalidades
- **Modo Vídeo (`video_mode`)**: Ativa o modo de vídeo para processamento (`TRUE`); (__linha 952__)
- **Modo Cinza (`gray_mode`)**: Converte o vídeo para escala de cinza (`TRUE`) ou para a escala de cores a HSV (`FALSE`); (__linha 945__)
- **Atraso (`delay`)**: Define o atraso entre os quadros do vídeo (Se inserir `200` 🠊 200ms = 0.2 segundos por *frame*, por exemplo); (__linha 1019__)
- ***Frame* Inicial (`starting_frame`)**: Define a *frame* inicial para o processamento do vídeo (De `0` a `1800`). (__linha 1017__)

**AVISO**: O `video_mode` só funciona quando `gray_mode` está definido como FALSE. Se `gray_mode` estiver TRUE, o modo vídeo não estará disponível.

## Funções utilizadas
- **is_point_in_circle(x, y, cx, cy, r)**: Verifica se um ponto (x, y) está dentro do círculo com centro (cx, cy) e raio r.
- **agrupar_linhas(lines, pos_cir_x, pos_cir_y, raio, angle_threshold=12, proximity_threshold=20)**: Agrupa linhas próximas e quase paralelas. Utiliza as variáveis `lines` (linhas detectadas), `pos_cir_x` e `pos_cir_y` (coordenadas do centro do círculo), `raio` (raio do círculo), `angle_threshold` (tolerância de ângulo) e `proximity_threshold` (tolerância de proximidade).
- **distance_between_parallel_lines(line1, line2)**: Calcula a distância entre duas linhas paralelas. Utiliza `line1` e `line2` (linhas a serem comparadas).
- **detetar_ponteiros(grupos, pos_cir_x, pos_cir_y, ponteiro_segundos)**: Detecta os ponteiros do relógio. Utiliza `grupos` (grupos de linhas), `pos_cir_x` e `pos_cir_y` (coordenadas do centro do círculo), e `ponteiro_segundos` (booleano para indicar se é o ponteiro dos segundos).
- **get_hands(hands)**: Determina os ponteiros de hora, minuto e segundo a partir dos ponteiros detectados. Utiliza `hands` (lista de ponteiros).
- **get_hands_V(hands, second_hand)**: Determina os ponteiros de hora e minuto a partir dos ponteiros detectados. Utiliza `hands` (lista de ponteiros) e `second_hand` (ponteiro dos segundos).
- **get_hands_S(hands)**: Determina o ponteiro dos segundos a partir dos ponteiros detectados. Utiliza `hands` (lista de ponteiros).
- **calculate_rect_coordinates(line)**: Calcula as coordenadas de um retângulo ao redor de uma linha. Utiliza `line` (linha a ser envolvida).
- **draw_ponteiros_frame(img, hour_hand, minute_hand, second_hand)**: Desenha um retângulo e rótulos para os ponteiros do relógio na imagem. Utiliza `img` (imagem), `hour_hand` (ponteiro das horas), `minute_hand` (ponteiro dos minutos) e `second_hand` (ponteiro dos segundos).
- **get_vector(hand)**: Calcula o vetor direcional de um ponteiro do relógio. Utiliza `hand` (ponteiro do relógio).
- **dot_product(u, v)**: Calcula o produto escalar de dois vetores. Utiliza `u` e `v` (vetores).
- **cross_product(u, v)**: Calcula o produto vetorial de dois vetores. Utiliza `u` e `v` (vetores).
- **get_angle(hand, center_x, center_y)**: Calcula o ângulo de um ponteiro do relógio em relação ao eixo y. Utiliza `hand` (ponteiro do relógio), `center_x` e `center_y` (coordenadas do centro do relógio).
- **get_time(hour_angle, minute_angle, second_angle)**: Calcula o tempo a partir dos ângulos dos ponteiros do relógio. Utiliza `hour_angle` (ângulo do ponteiro das horas), `minute_angle` (ângulo do ponteiro dos minutos) e `second_angle` (ângulo do ponteiro dos segundos).
- **draw_time(img, time)**: Desenha o tempo na imagem do relógio. Utiliza `img` (imagem) e `time` (tempo calculado).
- **detect_region_of_interest(detect_circles, image, gray_mode, video_mode)**: Detecta a região de interesse (círculo) na imagem. Utiliza `detect_circles` (círculos detectados), `image` (imagem), `gray_mode` (modo de escala de cinza) e `video_mode` (modo de vídeo).
- **detect_ponteiros(image, S_image, V_image, masked_image, pos_cir_x, pos_cir_y, raio_cir, gray_mode, video_mode)**: Detecta os ponteiros do relógio na imagem. Utiliza `image` (imagem), `S_image` e `V_image` (componentes da imagem HSV), `masked_image` (imagem mascarada), `pos_cir_x` e `pos_cir_y` (coordenadas do centro do círculo), `raio_cir` (raio do círculo), `gray_mode` (modo de escala de cinza) e `video_mode` (modo de vídeo).
- **main()**: Função principal que executa o processamento de imagens ou vídeos para detectar os ponteiros do relógio e calcular o tempo.



## Contato

Para mais informações, entre em contato pelos email: [juda.imbo99@gmail.com](mailto:juda.imbo99@gmail.com)
