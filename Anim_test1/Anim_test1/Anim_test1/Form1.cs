using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.Net;
using System.IO;

namespace Anim_test1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        struct node
        {
            public int x;
            public int y;
            public int x_move;
            public int y_move;
           
        }
        private void Form1_Load(object sender, EventArgs e)
        {
            //將要取得HTML原如碼的網頁放在WebRequest.Create(@”網址” )
            //WebRequest myRequest = WebRequest.Create(@"http://keyfunapp.net/anime/tv.html");
            WebRequest myRequest = WebRequest.Create(@"http://pagead2.googlesyndication.com/pagead/show_ads.js");
            
            //Method選擇GET
            myRequest.Method = "GET";

            //取得WebRequest的回覆
            WebResponse myResponse = myRequest.GetResponse();

            //Streamreader讀取回覆
            StreamReader sr = new StreamReader(myResponse.GetResponseStream());
            
            //將全文轉成string
            string result = sr.ReadToEnd();

            //關掉StreamReader
            sr.Close();

            //關掉WebResponse
            myResponse.Close();

            //搜尋頭尾關鍵字, 搜尋方法見後記(1)
            //int first = result.IndexOf("美元 = <em>");
            //int last = result.LastIndexOf("</em> 新台幣");
            int first = result.IndexOf("星期日 ");
            int last = result.LastIndexOf("Copyright ");

            //減去頭尾不要的字元或數字, 並將結果轉為string. 計算方式見後記(2)
           // string HTMLCut = result.Substring(first + 9, last - first - 9);

            //string HTMLCut = result.Substring(first, last);
            string HTMLCut = result.Substring(1);

            Console.Write(HTMLCut);
            //txtRate.Text = HTMLCut;
        }
    }
}
