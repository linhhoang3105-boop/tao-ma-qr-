import streamlit as st
import zipfile
import qrcode
import io

# ==========================================
# CẤU HÌNH GIAO DIỆN XANH LÁ MÁT MẮT
# ==========================================
st.set_page_config(
    page_title="App Nén File & Tạo Mã QR - Hệ Mộc",
    page_icon="🌿",
    layout="centered"
)

# Thêm CSS để đổi màu chủ đạo thành xanh lá và trang trí
st.markdown("""
    <style>
    /* Nền màu xanh lá cực nhạt và text xanh lá đậm */
    .stApp {
        background-color: #f2fff2; 
        color: #004d00; 
    }
    
    /* Trang trí các khối card xanh matcha */
    .stCard {
        background-color: #e8f5e9; /* Xanh lá nhạt mát mắt */
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #a5d6a7;
        margin-bottom: 20px;
        position: relative; /* Cho phép đặt icon cây kiếm */
    }
    
    /* Trang trí cây kiếm và chiếc lá ở góc card */
    .stCard::after {
        content: '🗡️🍃';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 1.5em;
        opacity: 0.8;
    }

    /* Đổi màu tiêu đề xanh forest */
    h1, h2, h3 {
        color: #2e7d32 !important;
    }
    
    /* Đổi màu nút bấm xanh lá nổi bật */
    .stButton>button {
        background-color: #4caf50;
        color: white !important;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #388e3c;
        transform: scale(1.05);
    }
    
    /* Đổi màu viền ô nhập liệu */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #a5d6a7;
    }
    
    /* Căn chỉnh khung kéo thả file */
    .upload-box {
        background-color: white; 
        padding: 10px; 
        border-radius: 10px; 
        border: 1px dashed #4caf50;
    }
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# TIÊU ĐỀ CHÍNH VÀ BIỂU TƯỢNG CÂY KIẾM
# ==========================================
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    st.markdown("<h1 style='text-align: center; font-size: 3.5em; margin-top: 10px;'>🗡️</h1>", unsafe_allow_html=True)
with col_header2:
    st.title("App Nén File & Tạo Mã QR")
    st.write("---")
    st.markdown("<p style='text-align: left; font-style: italic; color: #404040;'>Chào mừng bạn đến với phiên bản 'Thanh Kiếm Xanh'! Ứng dụng gom gọn tài liệu và tạo mã QR siêu tốc, dịu mắt và cực kỳ xịn xò.</p>", unsafe_allow_html=True)

# ==========================================
# PHẦN 1: GOM FILE (CÓ TRANG TRÍ CARD)
# ==========================================
st.markdown("<div class='stCard'>", unsafe_allow_html=True)
st.header("📁 Bước 1: Gom các file thành tệp ZIP")

st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
uploaded_files = st.file_uploader("Kéo thả hoặc bấm để chọn các file cần nén:", accept_multiple_files=True)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for uploaded_file in uploaded_files:
            zip_file.writestr(uploaded_file.name, uploaded_file.getvalue())
    
    st.success(f"🎉 Xuất sắc! Đã gom xong {len(uploaded_files)} file vào tệp nén.")
    
    st.download_button(
        label="📥 Tải tệp ZIP về máy",
        data=zip_buffer.getvalue(),
        file_name="TaiLieu_DaNen.zip",
        mime="application/zip"
    )
    st.info("💡 Hướng dẫn: Tải file ZIP này về -> Upload lên Google Drive của bạn -> Copy 'Link chia sẻ công khai' nhé!")
st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# PHẦN 2: TẠO QR (MÃ QR CŨNG MÀU XANH)
# ==========================================
st.markdown("<div class='stCard'>", unsafe_allow_html=True)
st.header("🔗 Bước 2: Tạo Mã QR từ đường link")

link_input = st.text_input("Dán link chia sẻ (Google Drive, OneDrive...) vào đây:", placeholder="https://drive.google.com/...")

if link_input:
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(link_input)
        qr.make(fit=True)
        
        # Đổi màu mã QR thành xanh lá đậm cho tone sur tone
        img = qr.make_image(fill_color="#1b5e20", back_color="white") 
        
        qr_buffer = io.BytesIO()
        img.save(qr_buffer, format="PNG")
        
        col_qr1, col_qr2 = st.columns([2, 3])
        with col_qr1:
            st.image(qr_buffer.getvalue(), caption="Mã QR Hệ Mộc của bạn 🌿", width=250)
        with col_qr2:
            st.write("### Tuyệt vời quá!")
            st.write("Mã QR xanh mướt của bạn đã ra lò. Tải về và đi khoe thôi!")
            st.download_button(
                label="💾 Tải ảnh Mã QR về máy",
                data=qr_buffer.getvalue(),
                file_name="MaQR_XanhLa.png",
                mime="image/png"
            )
        
        st.balloons()
        st.markdown("<p style='text-align: center; color: #a5d6a7;'>🗡️🍃✨</p>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Ối, có lỗi xảy ra rồi: {e}")
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# CHÂN TRANG (FOOTER)
# ==========================================
st.write("---")
st.markdown("<p style='text-align: center; color: #8c8c8c; font-size: 0.85em;'>© 2026 Phiên bản Thanh Kiếm Xanh | Đưa code lên mây cùng Streamlit.</p>", unsafe_allow_html=True)
