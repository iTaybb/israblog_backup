// Edited by Itay Brandes 2017.12.22

function closePingFrame(frameID)
{
 		var iframeID = "PingFrame" + frameID.toString();
		var linkID = "PingFrameLink" + frameID.toString();
		document.getElementById(iframeID).style.display = "none";
		document.getElementById(linkID).style.display = "none";
}
function addToFavPosts(blogCode, postCode, postTitle)
{
	 	var url = "/edit/addtofavposts.asp?blog=";
		url += blogCode;
		url += "&blogcode=";
		url += postCode;
		url += "&posttitle=";
		url += postTitle;
		openWindow(url, 'addFav', 'scrollbars,resizable,width=500,height=400');		
}
 
function postsByCat(sBlogCatDesc, nBlogID)
{
    var strURL = "/postsbycat.asp?catdesc=";
	strURL += sBlogCatDesc;
	strURL += "&blog=";
	strURL += nBlogID;
	document.write("<a class='blog' href='" + strURL + "'>���</a>");
}
function randOrd(){
return (Math.round(Math.random())-0.5); } 

function displayTags(arrTag, strListOptions, isSameWindow, nMaxItems, oContainer)
{
 	var nArrSize = arrTag.length;
	var nArrIndex = 0;
	var nArrMin = 0;
	if (nMaxItems != 0)
	    nArrMin = nArrSize - nMaxItems;
	var maxTagSize = 0;
	var minTagSize = 10000;
	var nTagSize = 0;
	var sTarget = "";
	if ((isSameWindow == "0") || (isSameWindow == "False"))
	   sTarget = "_blank";
	if (strListOptions.indexOf("cloud=1") != -1)
	{
	    maxTagSize = arrTag[nArrSize - 1][2];
	    minTagSize = arrTag[0][2];
	    for (nArrIndex = 0; nArrIndex < nArrMin; nArrIndex++)
			arrTag[nArrIndex] = null;
		arrTag.sort(randOrd);
		for (nArrIndex = nArrSize - 1; nArrIndex >= 0; nArrIndex--)
		{
		   if (arrTag[nArrIndex])
		   {
		   	  nTagSize = eval(arrTag[nArrIndex][2]);
		   	  nTagSize = 12 + 30 * (nTagSize - minTagSize) / (maxTagSize - minTagSize);
		   	  nTagSize = Math.round(nTagSize); 
		   	  document.write("<a class='listag' style='font-size: " + nTagSize.toString() + "px;' target='" + sTarget + "' href='" + arrTag[nArrIndex][1] + "&catdesc=" + arrTag[nArrIndex][0].replace(/^\s+|\s+$/g,"") + "'>" + arrTag[nArrIndex][0].replace(/^\s+|\s+$/g,"") + "</a>  ");
		   } 
		}
	}
	else
	{	if (nArrMin < 0 ) 
			nArrMin = 0 ;
		for (nArrIndex = nArrSize - 1; nArrIndex >= nArrMin; nArrIndex--)
		{
		   document.write("<a class='list' target='" + sTarget + "' href='" + arrTag[nArrIndex][1] + "&catdesc=" + escape(arrTag[nArrIndex][0].replace(/^\s+|\s+$/g,"")) + "'>" + arrTag[nArrIndex][0].replace(/^\s+|\s+$/g,"") + " (" + arrTag[nArrIndex][2] + ")</a><br />"); 
		}
	}
}

function saveText(postCode, blogCode, isExcerpt)
{
 	var editID = "edit" + postCode.toString();
	var sText = document.getElementById(editID).innerHTML;
	if (sText.replace(/^\s+|\s+$/g,"") == '')
	{
	   alert("��� ����� ��� ���");
	   return;
	}
	document.frmInEdit.PostCode.value = postCode;
	document.frmInEdit.BlogCode.value = blogCode;
	document.frmInEdit.PostText.value = sText;
	document.frmInEdit.IsExcerpt.value = isExcerpt;
	document.frmInEdit.submit();
}

function editPostInline(postCode)
{
    var editID = "edit" + postCode.toString();
	var linksID = editID + "links";
	var sText = document.getElementById(editID).innerHTML;
	document.getElementById(editID).contentEditable = true;
	document.frmInEdit.OrigText.value = sText;
	document.getElementById(editID).style.borderStyle = "dotted";
	document.getElementById(linksID).style.display = "block";
}

function unDoText(postCode)
{
    var editID = "edit" + postCode.toString();
	var linksID = editID + "links";
	var sText = document.frmInEdit.OrigText.value;
	document.getElementById(editID).innerHTML = sText;
	document.getElementById(editID).contentEditable = false;
	document.frmInEdit.PostText.value = sText;
	document.getElementById(editID).style.borderStyle = "none";
	document.getElementById(linksID).style.display = "none";
}

function displayBoardName()
{
	return null;		
}
function readCookie(name)
{
	var nameEQ = name + "=";
	var ca = document.cookie.split(';');
	for(var i=0;i<ca.length;i++)
	{
		
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1,c.length);
		if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
	}
	
	return null;
}
function drawPageLink(blogid,BlogCat,BlogCatDesc,pageShift,pageNum){
	var sCaption = "��� ���";
	if (pageShift == -1)
	   sCaption = "��� �����";

	var url="?blog="+blogid+"&catcode="+BlogCat+"&pagenum="+pageNum+"&catdesc="+BlogCatDesc;
	document.write("<a class=blog href='"+url+"'>"+sCaption+"</a>")
}
function drawNavigateLink(blogid,BlogCat,BlogYear,BlogMonth,BlogDay,position,page,BlogCatDesc){
	var url;
	if(position==page)
		document.write(page+"      ")
	 else
			{		
			url="?blog="+blogid+"&catcode="+BlogCat+"&year="+BlogYear+"&month="+BlogMonth+"&day="+BlogDay+"&pagenum="+position+"&catdesc="+escape(BlogCatDesc)
			document.write("<a class=blog href='"+url+"'>"+position+"</a>&nbsp;&nbsp;")
			}
}

function drawMonthLinkNew(monthShift, CurrMonth, FirstMonth, LastMonth, blogid,BlogYear,BlogMonth, NextMonth, PrevMonth)
{
	var sCaption = "����� �����";
	if (monthShift == -1)
	{
	   if (CurrMonth <= FirstMonth)
	   	  return;
	   BlogMonth = PrevMonth.getMonth();
	   BlogYear = PrevMonth.getFullYear();
	}
	else
	{
	   if (CurrMonth >= LastMonth)
	   	  return;
	   sCaption = "����� ���";
	   BlogMonth = NextMonth.getMonth();
	   BlogYear = NextMonth.getFullYear();
	}
	BlogMonth++;
	sCaption += " (";
	sCaption += BlogMonth;
	sCaption += "/";
	sCaption += BlogYear;
	sCaption += ")";
	var url;
	url="?blog="+blogid+"&year="+BlogYear+"&month="+BlogMonth;
	document.write("<a class=blog href="+url+">"+ sCaption+"</a>&nbsp;&nbsp;");
}

function drawMonthLink(monthShift, CurrMonth, FirstMonth, LastMonth, blogid,BlogYear,BlogMonth)
{
	var sCaption = "����� �����";
	if (monthShift == -1)
	{
	   if (CurrMonth <= FirstMonth)
	   	  return;
	}
	else
	{
	   if (CurrMonth >= LastMonth)
	   	  return;
	   sCaption = "����� ���";
	}

	BlogMonth += monthShift;
	if (BlogMonth == 0)
	{
	   BlogMonth = 12;
	   BlogYear--;
	}
	if (BlogMonth == 13)
	{
	   BlogMonth = 1;
	   BlogYear++;
	}
	sCaption += " (";
	sCaption += BlogMonth;
	sCaption += "/";
	sCaption += BlogYear;
	sCaption += ")";
	var url;
	url="?blog="+blogid+"&year="+BlogYear+"&month="+BlogMonth;
	document.write("<a class=blog href="+url+">"+ sCaption+"</a>&nbsp;&nbsp;");
}
function drawSearchNavigateLink(q,s,position,page,title,bid){
	var url = "";
	if (bid=="0")
	   bid = "";
	if(position==page)
		document.write(page+"      ");
	 else
			{		
			url="?q="+q+"&s="+s+"&bid="+bid+"&hasbid=";
			if (bid != '')
			   url += "1";
			else
			   url += "0";
			url += "&pagenum="+position;
			if (title != "")
			   position = title;
			document.write("<a class=blog href="+url+">"+position+"</a>&nbsp;&nbsp;");
			}
}
function EditPost(postCode) {
    //OLD VERSION
	//document.frmEdit.code.value = postCode;
    //document.frmEdit.submit();
    //NEW VERSION BY BASHIR:09/08/2010
    window.open("edit/myblog.asp?edit=1&action=edit&postCode=" + postCode, "_self");
}
function showPointers(blogCode, userCode)
			  {
			   	 var url = '';
				 url = "/pointers.asp?blog=";
				 url += blogCode;
				 url += "&user=";
				 url += userCode;
		   		 openWindow(url,'commentWnd','height=400,width=600,scrollbars=yes,status=yes,resizable=yes');
			  }
 function addComment(blogCode, userCode)
			  {
			   	 openCommentWnd(blogCode, 1, userCode, '');
			  }
function getCommentsURL(blogCode, newComment, userCode, commentID)
{
			   	 var url = '';
				 url = "comments-";
				 url += blogCode;
				 url += "-p1.htm";
				 //url += "&blog=";
				 //url += blogCode;
				 //url += "&user=";
				 //url += userCode;
				 //url += "&commentuser="+userCode+"&origcommentuser="+userCode + "#" + commentID;
				 return url;
}
 function openCommentWnd(blogCode, newComment, userCode, commentID)
			  {
			   	var url = getCommentsURL(blogCode, newComment, userCode, commentID);
				window.open(url, '_blank', 'height=400,width=600,scrollbars=yes,status=yes,resizable=yes');
			  }
function showCommentsHere(blogCode, userCode)
{
	   	var strURL = getCommentsURL(blogCode, 0, userCode, ''); 			
		if (document.getElementById("frm" + blogCode))
		{
		   if (document.getElementById("frm" + blogCode).src.indexOf("comment") != -1)
		   {
	   	   	   document.getElementById("frm" + blogCode).src = '';
	       	   document.getElementById("frm" + blogCode).style.height = 0;
		   	   document.getElementById("frm" + blogCode).style.width = 0;
			   document.getElementById("frm" + blogCode).style.display = 'none';
		   }
		   else
		   {
	   	   	   document.getElementById("frm" + blogCode).src = strURL;
	       	   document.getElementById("frm" + blogCode).style.height = '400px';
		   	   document.getElementById("frm" + blogCode).style.width = '95%';
			   document.getElementById("frm" + blogCode).style.display = 'block';
		   }
		}
}

function showComments(blogCode, userCode)
			  {
			   	 openCommentWnd(blogCode, 0, userCode, '');
			  }
function showLastComments(blogCode, userCode,commentID)
			  {
			   	 var url = '';
				 url = "/comments.asp?newcomment=0";
				 url += "&blog=";
				 url += blogCode;
				 url += "&user=";
				 url += userCode;
				 url += "&commentuser="+userCode+"&direct="+commentID + "#" + commentID;
				 openWindow(url,'commentWnd','height=400,width=600,scrollbars=yes,status=yes,resizable=yes');
			  }
 function openSendToWin(blogName, blogCode)
			  {
			   	 var url = "/sendto.asp?blogcode=";
				 url += blogCode;
				 url += "&blogname=";
				 url += blogName;
				 openWindow(url,'sendToWnd','height=300,width=500,scrollbars=yes');
			  }
			 
 function goToLink(strURL, isSameWnd)
			  {
//				  if ((strURL != '') && (strURL.substring(0, 7) == 'http://'))
				   if (strURL != '') 
				  {
				   	 if (isSameWnd)
					 	document.location.href = strURL;
				   	 else
					 	openWindow(strURL, 'newWin','toolbar,menubar,scrollbars,resizable,status,location');
				  }
			  }
 function DisplayFullPathImg(ImgPath){
	if(ImgPath.indexOf('upload1'))
	document.write(ImgPath.replace('upload1','/upload1')) ;	
 }
 function removeTags(textValue)
			  {
			   		var textTemp = "";   
					while (textValue.indexOf('<') != -1)
					{
					   if (textValue.indexOf('>') < textValue.indexOf('<'))
					   	  return textValue;
					   else
					   {
					   	   textTemp = textValue.substring(0, textValue.indexOf('<'));
					   	   textValue = textTemp + textValue.substring(textValue.indexOf('>') + 1);
					   }
					}
					while (textValue.indexOf('&lt;') != -1)
					{
					   if (textValue.indexOf('&gt;') == -1)
					   	  return textValue;
					   else
					   {
					   	   textTemp = textValue.substring(0, textValue.indexOf('&lt;'));
					   	   textValue = textTemp + textValue.substring(textValue.indexOf('&gt;') + 1);
					   }
					}
					while (textValue.indexOf('&LT;') != -1)
					{
					   if (textValue.indexOf('&GT;') == -1)
					   	  return textValue;
					   else
					   {
					   	   textTemp = textValue.substring(0, textValue.indexOf('&LT;'));
					   	   textValue = textTemp + textValue.substring(textValue.indexOf('&GT;') + 1);
					   }
					}
					return textValue;
			  }
 function sendBoardMsg(blogid)
			  {
				
				 var strName = document.frmBoard.boardname.value;
				 
//				 strName = strName.replace(/\"/g, "");
//				 strName = strName.replace(/&/g,"%26");
				 strName = removeTags(strName);
				 if (strName.replace(/^\s+|\s+$/g,"") == '')
				 {
				    alert("�� ��� ��� ����");
					document.frmBoard.boardname.focus();
					return;
				 }
				
				 var strEmail = document.frmBoard.boardemail.value;
				
				 strEmail = strEmail.replace(/\"/g, "");
				 strEmail = removeTags(strEmail);
				 if (!isValidEmail(strEmail, 1))
				 {
					document.frmBoard.boardemail.focus();
				 	return;
				 }
				 var strText = document.frmBoard.boardtext.value;
//				 strText = strText.replace(/\"/g, "");
				 strText = strText.replace(/\n/g, " ");
//				 strText = strText.replace(/&/g,"%26");
				 strText = removeTags(strText);
				 if (strText.replace(/^\s+|\s+$/g,"") == '')
				 {
				    alert("?�� ����� ���� ����");
					document.frmBoard.boardtext.focus();
					return;
				 }
				 if (strText.length > 255)
				 {
				    alert(".���� ���� �-255 ����");
					document.frmBoard.boardtext.focus();
					return;
				 }
				 strText = escape(strText);
				 var strURL = document.frmBoard.boardurl.value;
				 strURL = strURL.replace(/\"/g, "");
				 strURL = strURL.replace(/&/g,"%26");
				 strURL = removeTags(strURL);
				 document.frmBoard.boardtext.value = '';				  			  
			     var url = "/board_list.asp?blog="+blogid+"&insert=1&name=";
			     
				 url += strName;
				 url += "&email=";
				 url += strEmail;
				 url += "&url=";
				 url += strURL;
				 url += "&text=";
				 url += strText;
				 url += "&savedata=";
				
				 if (document.frmBoard.SaveData.checked)
				 	url += "1";
				 else
				 	url += "0";
				 if (document.all)
				 {
			         document.all.ifrmBoard.src = url;
				 	 document.all.ifrmBoard.focus();
				 }
				 else
				 {
			         document.getElementById("ifrmBoard").src = url;
				 	 document.getElementById("ifrmBoard").focus();
				 }
			  }

function displayBoardForm()
			  {
			     if (document.all)
				 {
				      if (document.all.boardform.style.display == 'none')
			   	 	  {
					   	 document.all.boardform.style.display = 'block';
						 document.all.boardcaption.innerText = "���� ����";
			   	 	  }
				 	  else
			   	      {
			   	 	     document.all.boardform.style.display = 'none';
						 document.all.boardcaption.innerText = "���� ���";
			   	      }
				 }
				 else
				 {
				      if (document.getElementById("boardform").style.display == 'none')
			   	 	  {
					   	 document.getElementById("boardform").style.display = 'block';
						 document.getElementById("boardcaption").innerHTML = "���� ����";
			   	 	  }
				 	  else
			   	      {
			   	 	     document.getElementById("boardform").style.display = 'none';
						 document.getElementById("boardcaption").innerHTML = "���� ���";
			   	      }
				 }
				 
			  }

 function gotoArchive(BlogToGo,BlogID)
	{
		var splitdate=BlogToGo.split("/")
		var month=splitdate[0];
		var year=splitdate[1];
		var url=year+'-'+month+'-p1.htm';
		window.location.href=url;
		
	}
 function helpRSS()
		{
			openWindow('/rss_help.htm', 'rssWin', 'resizable,width=500,height=600');		
		}
 function clickedRSS()
			  {
				  if (navigator.appVersion.indexOf("MSIE 6") != -1)
				  {
				   	 alert("����� ������ �� ������ ������� ����� ����� �� ����� ������� ���� ������ ������ ����\nRSS");
				  	 return false;
				  }
			  }
	  	function displayEmail(linkStyle, userName, userDomain, userText)
		{
		 	if (userText == '')
			   document.write("<a class='" + linkStyle + "' href=" + "'mai" + "lto:" + userName + "@" + userDomain + "'>" + userName + "@" + userDomain + "</a>");
			else 
			   document.write("<a class='" + linkStyle + "' href=" + "'mai" + "lto:" + userName + "@" + userDomain + "'>" + userText + "</a>"); 
		}
	    function countChars()
		{
			if (document.frmBoard.boardtext.value.length > 255)
			   alert("����� ����� ������ ������");
		}
		function addFavorite(blogCode)
		{
		 	actOnFavorites(1, blogCode);
		}
		function removeFavorite(blogCode)
		{
		 	actOnFavorites(0, blogCode);
		}
		function submitAfterConfirm()
		{
		 	if (confirmSubmit())
			{
			   if (!document.all)
			   	 	document.getElementById("saveLink").innerHTML = "���";  
			   else
			   	 	document.all.saveLink.innerText = "���";  
			   document.frmEmail.submit();
			}
		}
		function confirmSubmit()
		{
		 	if (isValidEmail(document.frmEmail.email.value, 0))
			{
			   if (document.frmEmail.join[0].checked)
			   {
			   	  if (confirm("�������: ����� ����� ��������� ��� ���� ����� ������ �� ��� �����\n?��� ������ ������ �����"))
			   	  	 return true;
			   	  else
			   	  	 return false;
			   }
			   return true;
			}
			return false;
		}
		function isValidEmail(strEmail, allowEmpty)
		{
			if ((strEmail.replace(/^\s+|\s+$/g,"") == '') && (allowEmpty == 1))
			   return true;
			if ((strEmail.replace(/^\s+|\s+$/g,"") == '') && (allowEmpty == 0))
			{
			   alert("�� ����� ����� ���� �������� �����");
			   return false;
			}
			if ((strEmail.indexOf('@') == -1) || (strEmail.indexOf('.') == -1)) 
			{
			   alert("�� ����� ����� ���� �������� �����");
			   return false;
			}
			return true;
		}

		function actOnFavorites(addBlog, blogCode)
		{
		 	var url = "";
			url = "/favorites.asp?add=";
			url += addBlog;
			url += "&blog=";
			url += blogCode;
			openWindow(url, 'myFav', 'resizable,width=300,height=440');		
		}
			  function showNearBlogs(blogCode, userTitle)
			  {
			   	 var url = "nearframe.asp?blog=";
				 url += blogCode;
				 url += "&title=";
				 url += userTitle;
				 parent.location.href = url; 
			  }
			  
			  
				/*
				function AdjustLinks()
				{
				
					var oElement=document.getElementsByTagName('a');
					for(var i=0;i<oElement.length;i++)
					{
						var sLink=new String();
						var sLink=oElement[i].href;
						var sLocation=location;
						
						if(sLink.indexOf('#',0)>=0||sLink==sLocation){
							
						}
						else 
						if(sLink.indexOf("javascript:")<0)
						{
							if(oElement[i].target=='')
								oElement[i].target='_top';
						}
					}
				}
			*/	 
