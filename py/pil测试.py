from PIL import Image, ImageFilter
# 打开一个jpg图像文件，注意是当前路径:
im = Image.open('tian.jpg')
im.show()
# 获得图像尺寸
w, h = im.size
print('image size: %sx%s' % (w, h))
# 缩放到50%:
im.thumbnail((w // 2, h // 2))
print('image to: %sx%s' % (w // 2, h // 2))
# 把缩放后的图像用jpeg格式保存:
im.save('jun.jpg', 'jpeg')

# 打开一个jpg图像文件，注意是当前路径:
im1 = Image.open('jun.jpg')
#im.close()
im1.show()

# 应用模糊滤镜:
im2 = im.filter(ImageFilter.BLUR)
im2.save('jun1.jpg', 'jpeg')
im2 = Image.open('jun1.jpg')
im2.show()