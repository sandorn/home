import wx 
  
#import the newly created GUI file 
import Demo  
class CalcFrame(demo.MyFrame1): 
   def __init__(self,parent): 
      demo.MyFrame1.__init__(self,parent)  
	#按键事件触发函数
   def btn_submit(self,event): 
      num = int(self.m_textCtrl1.GetValue()) 
      self.m_textCtrl2.SetValue (str(num*num)) 
 
def main():        
    app = wx.App(False) 
    frame = CalcFrame(None) 
    frame.Show(True) 
    #start the applications 
    app.MainLoop() 
 
if __name__ == '__main__':
    main()
