from PyQt5.Qt import *
import sys

# 1. 创建一个应用程序对象
app = QApplication(sys.argv)

# 2.控件的操作
# 2.1创建控件
window = QWidget()
# 2.2设置控件

window.setWindowTitle("QFrame-功能测试")
window.resize(500, 500)
window.move(400, 250)

frame = QFrame(window)
frame.resize(100, 100)
frame.move(100, 100)
frame.setStyleSheet("background-color: cyan;")

# 2.3展示控件
window.show()

# 3.应用程序的执行， 进入到消息循环
sys.exit(app.exec_())
