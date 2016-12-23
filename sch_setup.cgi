#!/usr/local/bin/perl
#   設定画面  main

require "cgi-lib.pl";

local($i,$j,$k,$ho,$tt) ; 


&ReadParse(\%webdata);


$cur_yy = $webdata{'yy'} ; 
$cur_mm = $webdata{'mm'} ; 
$mode =   $webdata{'mode'} ; 
$key =    $webdata{'key'} ;  #  編集対象となるデータ番号 新規の場合、日付
$add_ok = $webdata{'add_ok'} ; 
$edit_ok = $webdata{'edit_ok'} ; 
$edit_del = $webdata{'edit_del'} ; 
$cfg_ok = $webdata{'cfg_ok'} ; 
$ctype = $webdata{'ctype'} ; 


&display_main_menu;
exit;


sub display_main_menu {

$setup_cus = "<a href=\"sch_cus.cgi\">カスタマイズ</a>\n" ; 
$setup_item = "<a href=\"sch_item.cgi\">定型項目編集</a>\n" ; 
$setup_list = "<a href=\"sch_list.cgi\">データ一覧</a>\n" ; 
$setup_holi = "<a href=\"sch_holi.cgi\">休日設定</a>\n" ; 
$setup_down = "<a href=\"sch_down.cgi\">データのダウンロード</a>\n" ; 

print << "EOF";
Content-type: text/html;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<meta http-equiv="Content-Style-Type" content="text/css">
<title>sch追加</title>
<style type="text/css">
<!--
.ttl{
font-size : 14pt;
font-family : "ＭＳ 明朝";
font-weight : bold;
color : blue;
background-color : #b4f3fc;
border-top-width : 3px;
border-bottom-width : 3px;
border-top-style : solid;
border-bottom-style : solid;
border-top-color : yellow;
border-bottom-color : yellow;
}
-->
</style>
</head>
<body>
<center>
<table>
<tbody>
<tr>
<td width="100"></td>
<td class="ttl">*** 設定 ***</td>
<td width="100"></td>
</tr>
</tbody>
</table>
</center>
<br>
<br>
<center>

<table border="0" cellspacing="0" cellpadding="2">
  <tbody>
  <tr>
  <td bgcolor="#c700ff">
  <table cellspacing="2" border="0" cellpadding="15" bgcolor="#ffffff">
    <tr>
    <td bgcolor="#ffffff">
            $setup_cus<br>
            <br>
            $setup_list<br>
            <br>
            $setup_item<br>
            <br>
            $setup_holi<br>
            <br>
            日背景色<br>
            <br>
            $setup_down<br>
            <br>
            <form method="POST" enctype="multipart/form-data" action="sch_upload.cgi">
            データのアップロード<br>
            ファイル：<input type="file" name="filen"><br>
            <input type="submit" value="アップロード" name="upname">
            </form>
            <br>

            <a href="javascript:window.close()">終了</a>
    </td>
    </tr>
  </table>
</td>
</tr>
</tbody>
</table>

</center>
</body>
</html>
EOF
}


