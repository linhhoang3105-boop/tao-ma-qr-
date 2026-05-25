import streamlit as st
import zipfile
import qrcode
import io

# ==========================================
# CẤU HÌNH GIAO DIỆN XANH-TRẮNG MÁT MẮT
# ==========================================
st.set_page_config(
    page_title="App Nén File & Tạo Mã QR - Phiên bản 'Kiếm Hữu'",
    page_icon="🗡️",
    layout="centered"
)

# Thêm CSS để đổi màu chủ đạo thành xanh và trang trí
st.markdown("""
    <style>
    /* Nền trắng và text xanh */
    .stApp {
        background-color: white;
        color: #004d99; /* Xanh đậm cho chữ */
    }
    
    /* Trang trí các khối card xanh nhạt */
    .stCard {
        background-color: #e6f7ff; /* Xanh nhạt mát mắt */
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #b3e0ff;
        margin-bottom: 20px;
        position: relative; /* Cho phép đặt icon cây kiếm */
    }
    
    /* Trang trí cây kiếm lấp lánh ở góc card */
    .stCard::after {
        content: '🗡️✨';
        position: absolute;
        top: 10px;
        right: 15px;
        font_size: 1.5em;
        opacity: 0.6;
    }

    /* Đổi màu tiêu đề xanh */
    h1, h2, h3 {
        color: #0066cc;
    }
    
    /* Đổi màu nút bấm xanh */
    .stButton>button {
        background-color: #0073e6;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 25px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #0059b3;
        transform: scale(1.05);
    }
    
    /* Đổi màu ô nhập liệu */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #b3e0ff;
    }
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# TIÊU ĐỀ CHÍNH VÀ BIỂU TƯỢNG CÂY KIẾM
# ==========================================
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    st.markdown("<h1 style='text-align: center; font_size: 3em;'>🗡️</h1>", unsafe_allow_html=True)
with col_header2:
    st.title("App Nén File & Tạo Mã QR Công Nghệ")
    st.write("---")
    st.markdown("<p style='text-align: left; font-style: italic; color: #595959;'>Chào mừng bạn đến với phiên bản 'Kiếm Hữu'! Ứng dụng gom gọn tài liệu và tạo mã QR chia sẻ nhanh chóng, luôn đồng hành cùng thanh kiếm dễ thương.</p>", unsafe_allow_html=True)

# ==========================================
# PHẦN 1: GOM FILE (CÓ TRANG TRÍ CARD)
# ==========================================
st.markdown("<div class='stCard'>", unsafe_allow_html=True)
st.header("📁 Bước 1: Gom các file thành tệp ZIP")

# Ô kéo thả file với hilt (chuôi kiếm) pattern
st.markdown("<div style='background-color: white; padding: 10px; border-radius: 10px; border: 1px solid #b3e0ff;'>", unsafe_allow_html=True)
uploaded_files = st.file_uploader("Kéo thả hoặc bấm để chọn các file cần nén:", accept_multiple_files=True)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_files:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for uploaded_file in uploaded_files:
            zip_file.writestr(uploaded_file.name, uploaded_file.getvalue())
    
    st.success(f"🎉 Đã gom xong {len(uploaded_files)} file vào tệp nén!")
    
    st.download_button(
        label="📥 Tải tệp ZIP về máy của bạn",
        data=zip_buffer.getvalue(),
        file_name="TaiLieu_DaNen.zip",
        mime="application/zip"
    )
    st.info("💡 Hướng dẫn: Hãy tải file ZIP này về, sau đó mang lên Google Drive của bạn upload lên và lấy 'Link chia sẻ công khai' nhé!")
st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# PHẦN 2: TẠO QR (CÓ TRANG TRÍ CARD VÀ HIỆU ỨNG)
# ==========================================
st.markdown("<div class='stCard'>", unsafe_allow_html=True)
st.header("🔗 Bước 2: Tạo Mã QR từ đường link")

link_input = st.text_input("Dán link chia sẻ (Google Drive, OneDrive, Dropbox...) vào đây:", placeholder="https://drive.google.com/...")

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
        
        img = qr.make_image(fill_color="#004d99", back_color="white") # QR màu xanh đậm cho hợp tông
        
        qr_buffer = io.BytesIO()
        img.save(qr_buffer, format="PNG")
        
        col_qr1, col_qr2 = st.columns([2, 3])
        with col_qr1:
            st.image(qr_buffer.getvalue(), caption="Mã QR tài liệu của bạn", width=250)
        with col_qr2:
            st.write("### Tuyệt vời!")
            st.write("Mã QR của bạn đã sẵn sàng. Hãy tải về và gửi cho mọi người nhé.")
            st.download_button(
                label="💾 Tải ảnh Mã QR về máy",
                data=qr_buffer.getvalue(),
                file_name="MaQR_TaiLieu.png",
                mime="image/png"
            )
        
        # Thêm hiệu ứng chúc mừng lấp lánh hơn
        st.balloons()
        st.markdown("<p style='text-align: center; color: #ccf2ff;'>🗡️💫✨</p>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Có lỗi xảy ra khi tạo QR: {e}")
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# CHÂN TRANG (FOOTER)
# ==========================================
st.write("---")
st.markdown("<p style='text-align: center; color: #bfbfbf; font_size: 0.8em;'>© 2026 Phiên bản 'Kiếm Hữu' | Nền tảng mát mắt và mạnh mẽ.</p>", unsafe_allow_html=True)
