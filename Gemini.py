import streamlit as st 
import google.generativeai as genai 
import google.ai.generativelanguage as glm 
from dotenv import load_dotenv
from PIL import Image
import os 
import io 

#load_dotenv()

def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr=imgByteArr.getvalue()
    return imgByteArr

#API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key="GOOGLE_API_KEY")

st.image("./Google-Gemini-AI-Logo.png", width=200)
st.write("")

gemini_pro, gemini_vision = st.tabs(["Gemini Pro", "Gemini Pro Vision"])

def main():
    with gemini_pro:
        st.header("Gemini에게 물어 보세요! 😁")
        st.write("")

        prompt = st.text_input("아래에 질문을 작성하세요!", placeholder="Prompt", label_visibility="visible")
        model = genai.GenerativeModel("gemini-pro")

        if st.button("SEND",use_container_width=True):
            response = model.generate_content(prompt)

            st.write("")
            st.header(":blue[결과]")
            st.write("")

            st.markdown(response.text)

    with gemini_vision:
        st.header("Gemini Pro Vision에게 물어 보세요! 😎")
        st.write("")

        image_prompt = st.text_input("이미지와 관련된 질문을 적어 보세요!( ex)사진속 인물은 누구야? )", placeholder="Prompt", label_visibility="visible")
        uploaded_file = st.file_uploader("이미지 선택", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])

        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width=True)

            st.markdown("""
                <style>
                        img {
                            border-radius: 10px;
                        }
                </style>
                """, unsafe_allow_html=True)
            
        if st.button("응답 결과", use_container_width=True):
            model = genai.GenerativeModel("gemini-pro-vision")

            if uploaded_file is not None:
                if image_prompt != "":
                    image = Image.open(uploaded_file)

                    response = model.generate_content(
                        glm.Content(
                            parts = [
                                glm.Part(text=image_prompt),
                                glm.Part(
                                    inline_data=glm.Blob(
                                        mime_type="image/jpeg",
                                        data=image_to_byte_array(image)
                                    )
                                )
                            ]
                        )
                    )

                    response.resolve()

                    st.write("")
                    st.write(":blue[응답 결과]")
                    st.write("")

                    st.markdown(response.text)

                else:
                    st.write("")
                    st.header(":red[프롬프트를 작성해 주세요]")

            else:
                st.write("")
                st.header(":red[이미지를 업로드해 주세요]")

if __name__ == "__main__":
    main()
