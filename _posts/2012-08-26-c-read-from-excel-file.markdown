---
layout: post
title:  "C# Read from Excel file"
date:   2012-08-26 20:02:05 +0300
categories: files
thumbnail: /imgs/thumbnails/viewexcel.png
---

In this tutorial I'll show you how to use C# to read an **Excel** file's data. - no more than 10 lines of code - isn't .NET awesome ?

The method used is described below...

## Adding the reference

To read values from an Excel file, you need to add a reference:  
from Solution Explorer, right click on _References->Add reference->.NET_ and look for **Microsoft.Office.Interop.Excel**.

Once done, add the following line in your project:

{% highlight csharp linenos %}using Microsoft.Office.Interop.Excel;{% endhighlight %}

## Opening the document

First, we need an **Microsoft.Office.Interop.Excel.Application** object, so we can open the Excel file:

{% highlight csharp linenos %}Microsoft.Office.Interop.Excel.Application excel = new Microsoft.Office.Interop.Excel.Application();{% endhighlight %}

Once the file is opened, we have to store the data - this is done using an **WorkBook object**. This method has lots of arguments, fortunately only the first is required (which is the file's path) - so we can add Type.Missing to the others:

{% highlight csharp linenos %}Workbook wbook = excel.Workbooks.Open(Directory.GetCurrentDirectory() + "/" + "filename.xls", 
                     Type.Missing, Type.Missing, Type.Missing, 
                     Type.Missing, Type.Missing, Type.Missing, 
                     Type.Missing, Type.Missing, Type.Missing, 
                     Type.Missing, Type.Missing, Type.Missing, 
                     Type.Missing, Type.Missing);{% endhighlight %}

## Reading the data

Now, as you probably know, an **Excel document** contains multiple **WorkSheets**. To read a **cell's value**, we have to select the WorkSheet where the cell is found:

{% highlight csharp linenos %}Sheets worksheets = wbook.Worksheets;  //storing all the sheets

Range cell = ((Worksheet)worksheets["Sheet1"]).get_Range("A1", "A1");
//from the worksheets, we select Sheet1 and then the cell A1

string cell_value = cell.Value.ToString();  //this is the cell's value

/* some-code */

wbook.Close(); //closing...
{% endhighlight %}

## Result

That's all you might need to know about how to read an Excel document with C#.  
I wrote a small application which shows the content of a Excel file, using a **dataGridView**. It looks like this:

{% include image.html url="/imgs/posts/c-read-from-excel-file/1.png" description="Successfully Reading data from an Excel Spreadsheet" %}

And the code I wrote:

{% highlight csharp linenos %}using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using Microsoft.Office.Interop.Excel;
using System.IO;

namespace Excel
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            Microsoft.Office.Interop.Excel.Application excel = new Microsoft.Office.Interop.Excel.Application();

            Workbook wbook = excel.Workbooks.Open(Directory.GetCurrentDirectory() + "/" + "test.xls",
                     Type.Missing, false, Type.Missing,
                     Type.Missing, Type.Missing, Type.Missing,
                     Type.Missing, Type.Missing, Type.Missing,
                     Type.Missing, Type.Missing, Type.Missing,
                     Type.Missing, Type.Missing);

            Sheets worksheets = wbook.Worksheets;

            //note that ExcelGridView is a dataGridView
            for (char c = 'A'; c < 'E'; c++)
            {
                ExcelGridView.Columns.Add("col", c.ToString());
                for (int i = 1; i < 10; i++)
                {
                    string celladdr = c.ToString() + i.ToString();  //cell's address (like A1 or B5, etc.)
                    Range cell = ((Worksheet)worksheets["Sheet1"]).get_Range(celladdr, celladdr);

                    ExcelGridView.Rows.Add();

                    try
                    {
                        ExcelGridView.Rows[i - 1].Cells[(int)c - 65].Value = cell.Value.ToString();
                    }

                    catch { /*empty cell*/ }

                }
            }

            wbook.Close();

        }
    }
}
{% endhighlight %}