---
layout: post
title:  "C# Create Child Forms"
date:   2013-02-02 20:02:05 +0300
tags: c-sharp form
redirect_from: /interface/c-create-child-forms
image: /imgs/thumbnails/childforms.webp
---

**Child Forms** are those forms that are found inside another form (parent form). There are multiple ways to create child forms - most of them require to use a **MDI Container**.  
  

## Child Forms without MDI Container

I, personally, had lots of problems when I used it (parent form's controls were going over the child form), so I decided to create child forms without involving a MDI Container. This method will let you solve the problem with the controls that go over child forms, by allowing you to use **BringToFront()**.  

## How to:

The main trick here is to treat **child forms** as **Controls**. You'll create a child form just like any other control. When you use this method, you have to set it's **TopLevel** to **false** - otherwise it won't work.

The following lines of code are used to create a child form:

```csharp
Form childForm = new Form(); //initialize a child form

childForm.TopLevel = false; //set its TopLevel to false

Controls.Add(childForm); //and add it to the parent Form
childForm.Show(); //finally display it

childForm.BringToFront(); //use this to render your newly created form over the controls

```