import streamlit as st
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt

class_names = [
    "Футболка/топ", "Штани", "Светр", "Сукня", "Пальто", 
    "Сандалі", "Сорочка", "Кросівки", "Сумка", "Черевики"
]

st.title("Завантаження та класифікація зображення")

uploaded_file = st.file_uploader("Виберіть зображення...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Завантажене зображення", use_column_width=True)

    model_choice = st.selectbox('Оберіть модель', ["CNN", "VGG16"])

    if model_choice == "CNN":
        model_path = 'models/cnn_model.keras'

        resized_image = ImageOps.grayscale(image)
        resized_image = resized_image.resize((28, 28))
        input_array = np.array(resized_image) / 255.0
        input_array = np.expand_dims(input_array, axis=(0, -1))
    else:
        model_path = 'models/vgg16_model.keras'

        resized_image = image.resize((32, 32))
        input_array = np.array(resized_image) / 255.0
        if input_array.shape[-1] == 4:
            input_array = input_array[:, :, :3]
        elif input_array.shape[-1] == 1:
            input_array = np.repeat(input_array, 3, axis=-1)
        input_array = np.expand_dims(input_array, axis=0)

    try:
        model = tf.keras.models.load_model(model_path)
        st.success(f"Модель {model_choice} вдало завантажено!")
    except Exception as e:
        st.error(f"Помилка завантаження моделі {model_choice}: {e}")
        model = None

    if model is not None:
        predictions = model.predict(input_array)
        class_probabilities = predictions[0]
        predicted_class = np.argmax(class_probabilities)

        st.subheader("Ймовірності для кожного класу")
        for i, prob in enumerate(class_probabilities):
            st.write(f"{class_names[i]}: {prob:.2f}")

        st.subheader("Результат класифікації")
        st.write(f"Передбачений клас: {class_names[predicted_class]}")
        st.write(f"Ймовірність: {predictions[0][predicted_class]:.2f}")

        st.subheader("Графік ймовірностей для кожного класу")
        plt.figure(figsize=(8, 4))
        plt.bar(range(len(class_probabilities)), class_probabilities, tick_label=class_names)
        plt.title('Ймовірності для кожного класу')
        plt.xlabel('Назва класу')
        plt.ylabel('Ймовірність')
        st.pyplot(plt)
