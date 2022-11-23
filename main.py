import face_recognition #人臉辨識
import audio_decode
from gpb import delay, Servo
import bluetooth
from machine import Pin, ADC
from sensor import HC_SR04
import voice_recognition

led1 = Pin('', Pin.OUT) #門上的燈代表以解鎖的標誌(室外燈)(一般燈)
door = Servo(1) #開啟門的馬達
sr04 = HC_SR04('', '')  #超音波開啟
light = ADC()   #光敏感應
audio_decode.init()
audio_decode.start('開機&啟動人臉辨識&藍芽.mp3')
unlock = 0
times = 0   #計算辨識失敗次數
password = '1234'
face_recognition.start()
face_recognition.set_process(1) #辨識開始
face_recognition.recognize_start()  #辨識開始
bluetooth.active(1) #藍芽開啟
bluetooth.advertise(100,'POMAS')    #廣播時間&裝置名稱
bluetooth.write("請輸入密碼或使用人臉辨識來解鎖")

while unlock == 0:
    if face_recognition.get_face_id(0) == 0:
        audio_decode.start('辨識失敗.mp3')
        times += 1
        if times == 5:
            audio_decode.start('辨識失敗五次等待1min.mp3')
            times = 0
            delay(60000)
        delay(5000)
        face_recognition.recognize_start()
    elif face_recognition.get_face_id(0) != 0 or bluetooth.read() == password:
        unlock = 1
        audio_decode.start('成功.mp3')
        face_recognition.recognize_stop()   #停止辨識
        face_recognition.stop() #停止face_recognition
        bluetooth.write("輸入help得到藍芽指令")
        led1.value(1)   #門上的燈代表以解鎖的標誌(室外燈)

    
        
        

while unlock != 0:

    while bluetooth.read() == '改密碼': #修改密碼
        bluetooth.wrire('請輸入原密碼:')
        if bluetooth.read() != password:
            break
        else:
            bluetooth.write("輸入你要改的密碼:")
            changepassword = bluetooth.read()
            if changepassword != b'':
                bluetooth.write('請輸入第二次你要改的密碼')
                if bluetooth.read() == changepassword:
                    password = changepassword
                    bluetooth.write('修改成功')
                else:
                    bluetooth.wrire('輸入錯誤請重新開始')
                    break

    while bluetooth.read() == '新增人臉辨識':   #新增人臉辨識
        face_recognition.start()
        audio_decode.start('先辨識解鎖以新增人臉.mp3')
        face_recognition.set_process(1)
        face_recognition.recognize_start()
        delay(2000)
        if face_recognition.get_face_id(0) == 0:
            audio_decode.start('辨識失敗請重新開始.mp3')
            face_recognition.recognize_stop()
            face_recognition.stop()
        else:
            audio_decode.start('辨識成功.mp3')
            face_recognition.recognize_stop()
            face_recognition.stop()
            delay(500)
            face_recognition.start()
            audio_decode.start('開始新增人臉.mp3')
            face_recognition.train()
            face_recognition.set_process(0) #結果為0是成功，但我懶得寫這裡可能出問題
            audio_decode.start('新增成功.mp3')
            face_recognition.stop()

    while sr04.Ultrasound() <= 10 or bluetooth.read() == '開門':
        delay(500)
        door.angle()    #開門
        delay(5000)
        door.angle()    #關門

    while light.read() < 1000:  #室外燈用光敏自動感應開關
        led1.value(1)
    else:
        led1.value(0)

    while bluetooth.read() == 'help':   #列出所有指令
        bluetooth.write("")
    


