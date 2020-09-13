---
layout: post
title:  "C# Simple Syntax Highlighting"
date:   2013-08-17 20:02:05 +0300
tags: c-sharp syntax-highlighting
redirect_from: /interface/c-simple-syntax-highlighting
image: /imgs/thumbnails/syntaxhighlight.webp
---

Some time ago, I had to make a project that required **syntax highlighting** - luckily I wasn't the one who had to make that part. However the version used in the project was more complicated - so I decided to make a tutorial that will teach you how to make a _basic_ syntax highlighter (with **Regex**).

I'll be using the `RichTextBox` control - using the simple `TextBox` might seem to be better but it's kind of difficult to implement the word coloring function without getting into other troubles.

Anyhow it needs to be improved - I tried to keep things as simple as possible. This program is just to show you the basic idea behind a syntax highlighter.

## Preview

{% include image.html url="/imgs/posts/c-simple-syntax-highlighting/1.png" description="Preview of the custom highlighter" %}

## 1.How It Works:

This part is meant to explain the main idea behind the whole process. The algorithm will follow these steps **each time** the text in the **RichTextBox** changes:

1) **scan the content** using different Regex patterns

2) **store the original caret's position**, so we can go back from where we started, after the highlighting is done

3) **focus another control** - this is a trick that I know from a friend, you have to do this to avoid the blinking effect

4) **highlight!** - simply changing the SelectionColor...

5) **move the caret back & reset the color**

6) **restore focus** to the RichTextBox

Each Regex **Match** contains its position and its length - we'll need these for highlighting. All the matches are stored in a **MatchCollection** (list). At the end, there'll be multiple lists, as an example: there'll be a list that contains strings, another list that contains comments, etc.

## 2.Coding Part

The most complicated part is the Regex part - everything else should be pretty straightforward. And since the code is not that complicated, I'll post the complete source:

```csharp
using System;
using System.Drawing;
using System.Text.RegularExpressions;
using System.Windows.Forms;

namespace Highlighter
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();

        }

        private void codeRichTextBox_TextChanged(object sender, EventArgs e)
        {
            // getting keywords/functions
            string keywords = @"\b(public|private|partial|static|namespace|class|using|void|foreach|in)\b";
            MatchCollection keywordMatches = Regex.Matches(codeRichTextBox.Text, keywords);

            // getting types/classes from the text 
            string types = @"\b(Console)\b";
            MatchCollection typeMatches = Regex.Matches(codeRichTextBox.Text, types);

            // getting comments (inline or multiline)
            string comments = @"(\/\/.+?$|\/\*.+?\*\/)";   
            MatchCollection commentMatches = Regex.Matches(codeRichTextBox.Text, comments, RegexOptions.Multiline);

            // getting strings
            string strings = "\".+?\"";
            MatchCollection stringMatches = Regex.Matches(codeRichTextBox.Text, strings);

            // saving the original caret position + forecolor
            int originalIndex = codeRichTextBox.SelectionStart;
            int originalLength = codeRichTextBox.SelectionLength;
            Color originalColor = Color.Black;

            // MANDATORY - focuses a label before highlighting (avoids blinking)
            titleLabel.Focus();

            // removes any previous highlighting (so modified words won't remain highlighted)
            codeRichTextBox.SelectionStart = 0;
            codeRichTextBox.SelectionLength = codeRichTextBox.Text.Length;
            codeRichTextBox.SelectionColor = originalColor;

            // scanning...
            foreach (Match m in keywordMatches)
            {
                codeRichTextBox.SelectionStart = m.Index;
                codeRichTextBox.SelectionLength = m.Length;
                codeRichTextBox.SelectionColor = Color.Blue;
            }

            foreach (Match m in typeMatches)
            {
                codeRichTextBox.SelectionStart = m.Index;
                codeRichTextBox.SelectionLength = m.Length;
                codeRichTextBox.SelectionColor = Color.DarkCyan;
            }

            foreach (Match m in commentMatches)
            {
                codeRichTextBox.SelectionStart = m.Index;
                codeRichTextBox.SelectionLength = m.Length;
                codeRichTextBox.SelectionColor = Color.Green;
            }

            foreach (Match m in stringMatches)
            {
                codeRichTextBox.SelectionStart = m.Index;
                codeRichTextBox.SelectionLength = m.Length;
                codeRichTextBox.SelectionColor = Color.Brown;
            }

            // restoring the original colors, for further writing
            codeRichTextBox.SelectionStart = originalIndex;
            codeRichTextBox.SelectionLength = originalLength;
            codeRichTextBox.SelectionColor = originalColor;

            // giving back the focus
            codeRichTextBox.Focus();
        }
    }
}
```