import streamlit as st
import zipfile
import qrcode
import io

# Cấu hình tiêu đề trang web
st.set_page_config(page_title="App Nén File & Tạo Mã QR", page_icon="🚀", layout="centered")

st.title("🎬 App Nén File & Tạo Mã QR Công Nghệ")
st.write("Ứng dụng giúp bạn gom gọn tài liệu và tạo mã QR chia sẻ nhanh chóng.")

# ==========================================
# PHẦN 1: NÉN FILE TRÊN WEB
# ==========================================
st.markdown("---")
st.header("📁 Bước 1: Gom các file thành tệp ZIP")

# Ô kéo thả file trên giao diện web
uploaded_files = st.file_uploader("Kéo thả hoặc bấm để chọn các file cần nén:", accept_multiple_files=True)

if uploaded_files:
    # Tạo một file ZIP ảo trong bộ nhớ RAM
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for uploaded_file in uploaded_files:
            # Đọc dữ liệu của từng file và nén vào tệp ZIP
            zip_file.writestr(uploaded_file.name, uploaded_file.getvalue())
    
    st.success(f"🎉 Đã gom xong {len(uploaded_files)} file vào tệp nén!")
    
    # Nút bấm tải file ZIP về máy người dùng
    st.download_button(
        label="📥 Tải tệp ZIP về máy của bạn",
        data=zip_buffer.getvalue(),
        file_name="TaiLieu_DaNen.zip",
        mime="application/zip"
    )
    st.info("💡 Hướng dẫn: Hãy tải file ZIP này về, sau đó mang lên Google Drive của bạn upload lên và lấy 'Link chia sẻ công khai' nhé!")

# ==========================================
# PHẦN 2: TẠO MÃ QR TỪ LINK
# ==========================================
st.markdown("---")
st.header("🔗 Bước 2: Tạo Mã QR từ đường link")

# Ô nhập link chia sẻ
link_input = st.text_input("Dán link chia sẻ (Google Drive, OneDrive, Dropbox...) vào đây:")

if link_input:
    try:
        # Cấu hình mã QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(link_input)
        qr.make(fit=True)
        
        # Tạo ảnh QR
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Lưu ảnh QR vào bộ nhớ RAM để hiển thị và cho tải về
        qr_buffer = io.BytesIO()
        img.save(qr_buffer, format="PNG")
        
        # Hiển thị ảnh QR lên màn hình web
        st.image(qr_buffer.getvalue(), caption="Mã QR tài liệu của bạn", width=250)
        
        # Nút bấm tải ảnh QR về máy
        st.download_button(
            label="💾 Tải ảnh Mã QR về máy",
            data=qr_buffer.getvalue(),
            file_name="MaQR_TaiLieu.png",
            mime="image/png"
        )
        st.balloons() # Hiệu ứng bóng bay chúc mừng cho đẹp mắt
    except Exception as e:
        st.error(f"Có lỗi xảy ra khi tạo QR: {e}")
      
