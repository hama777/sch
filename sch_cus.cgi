#!/usr/local/bin/perl
# カレンダー表示サブ 
# とりあえずsjisで作成

# schdate   スケジュール日付 yyyymmdd
# schdate2  スケジュール終了日付 yyyymmdd
# schrep    繰り返し
# schadj    調整
# schfnt    フォント情報
# schitem   内容

# mode 0 .. スケジュール表示  1 .. 新規入力画面  2 .. 編集画面 
#      3 .. カスタマイズ画面  
# ctype 0 .. カレンダー型  1 .. 縦型2ヶ月表示  2 .. 縦型3ヶ月表示
#       3 .. 年間カレンダー  4 .. データ一覧   5 .. 週間  6 .. モバイル

require "cgi-lib.pl";

local($i,$j,$k,$ho,$tt) ; 

$version = "1.35" ; 

@monthday = ('31','28','31','30','31','30','31','31','30','31','30','31');
@wkname = ('日','月','火','水','木','金','土') ;
@cname = ("","#ff0000","#008740","#0000ff","#ffff00","#800080","#ff00ff","#00ffff","#ec9800","#ffffff","#000000" ) ; 
@cname2 = ("","赤","緑","青","黄","紫","シアン","水","橙","白","黒" ) ; 

@fixed_item = ("会議","休暇") ; 

#open (DDD,"> debug.txt");
#close(DDD) ;

$line_color = "#009500" ;   # 線の色
$normal_bg =  "#ffffff" ;   # 通常のセル背景色
$ho_bg =      "#fed0e0" ;   # 休日のセル背景色
$ot_bg =      "#dcdcdc" ;   # 月外のセル背景色
$yo_bg =      "#fff200" ;   # 曜日のセル背景色
$today_bg =   "#cbffff" ;   # 今日のセル背景色
$sat_bg =     "#e8f2f9" ;   # 土曜日のセル背景色
$ho_num_cl =      "#ff0000" ;   # 休日の日付の色
$sat_num_cl =     "#0000ff" ;   # 土曜日の日付の色
$normal_num_cl =  "#000000" ;   # 通常の日付の色
$ho_num_bg =      "#f9ff91" ;   # 休日の日付の背景色
$sat_num_bg =     "#f9ff91" ;   # 土曜日の日付の背景色
$normal_num_bg =  "#f9ff91" ;   # 通常の日付の背景色
$pri_ho_bg =      "#fcaac9" ;   # 私休日のセル背景色
 

$line_width =  1    ;       # 線の幅
$cellpadding = 2   ;        # セル内余白
$border =      0        ;   # 線のボーダー
$out_line_width = 0    ;    # 外枠 線の幅
$bgcolor =    "#ffffff" ;   # カレンダー外、背景色
$cursor_bg =  "#ccffcc" ;   # カーソルがあるセルの背景色

$width = 100 ;              # カレンダー項目の幅
$height= 80 ;               # カレンダー項目の高さ
$align = "left" ; 
$valign = "top" ;
$start_wk = 1   ;           # 開始曜日  1 .. 月曜日
$schlen = 99     ;          # 月スケジュール 1項目の長さ
$max_itemcnt = 3 ;          # カレンダーに表示する1日の項目最大数
$width_2month = 500 ;       # 2ヶ月表示 幅
$cellpadding_3month = 200 ; # 3ヶ月表示 幅
$cellpadding_2month = 1 ;   # 2ヶ月表示 セル内余白

$main_char_size = 9 ;       # カレンダー型 文字サイズ
$mini_char_size = 11 ;      # ミニカレンダー 文字サイズ
$year_char_size = 10 ;      # 年間レンダー 文字サイズ(未使用)
$list_char_size = 9 ;       # 縦型カレンダー 文字サイズ
$daynumber_size = 10 ;      # 日付文字のサイズ

                            # 日のフォーマット
$fmt_ho="<td bgcolor=%s align=%s valign=%s class=sc onClick=\"add(%d,%d)\"><font color=red>%d</font></td>\n" ; 
$fmt_nm="<td bgcolor=%s align=%s valign=%s class=sc onClick=\"add(%d,%d)\">%s</td>\n" ; 

$fmt_menu="<a href=\"sch.pl?ctype=%d&yy=%d&mm=%d\">%s</a> \n" ; 


$mode = 0 ; 
$ctype = 0 ; 

&ReadParse(\%webdata);


$cfg_ok = $webdata{'cfg_ok'} ; 
$cfg_ng = $webdata{'cfg_ng'} ; 

if ( $mode == 3  )  {   #  カスタマイズ画面
    &display_cfg ; 
    exit ; 
}

#本日の日付を取得
$tt = time() ; 
($dm,$dm,$dm,$today_dd,$today_mm,$today_yy,$dm,$dm,$dm) = localtime($tt);
$today_yy = $today_yy + 1900;  
$today_mm = $today_mm + 1 ;

if ( $cur_mm == 0 ) { 
    $cur_mm = $today_mm ;  $cur_yy = $today_yy ;
}



################### test
#$ctype = 6 ; 

#&display_week ; 
#exit ; 

#$ctype = 2 ; 
#$mode = 5 ; 
#&display_list ; 
#&display_edit(13) ; 
#exit ;
###################

&read_cfg ;


if ( $cfg_ok ne ""  )  {   #  カスタマイズ処理
    &edit_cfg ; 
    &w_close ;
#    &message;
#    system("./sch.pl?ctype=0") ; 
    exit ; 
}

if ( $cfg_ng ne ""  )  {   #  カスタマイズ処理
    &w_jump ;
#    &message;
#    system("./sch.pl?ctype=0") ; 
    exit ; 
}

#printf(DBG  "display\n") ; 
#close(DBG) ;

&display_cfg ;
exit ; 

sub w_close {
print << "EOF";
Content-type: text/html;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<meta http-equiv="Content-Style-Type" content="text/css">
<title>設定完了</title>
</head>
<body  onload="javascript:window.close()">
</body>
</html>
EOF

}

sub w_jump {
print << "EOF";
Content-type: text/html;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<meta http-equiv="Content-Style-Type" content="text/css">
<title>設定完了</title>
</head>
<body  onload="javascript:window.open('./sch_setup.pl',_self)">
</body>
</html>
EOF

}

sub message {
print << "EOF";
Content-type: text/html;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<meta http-equiv="Content-Style-Type" content="text/css">
<title>設定完了</title>
</head>
<body>
設定完了
</body>
</html>
EOF

}

sub edit_cfg {
local($s) ;
open (OUT,"> schcfg.txt");
printf(OUT "line_color=%s\n",$webdata{'line_color'}) ; 
printf(OUT "normal_bg=%s\n",$webdata{'normal_bg'}) ; 
printf(OUT "today_bg=%s\n",$webdata{'today_bg'}) ; 
printf(OUT "holiday_bg=%s\n",$webdata{'holiday_bg'}) ; 
printf(OUT "other_bg=%s\n",$webdata{'other_bg'}) ; 
printf(OUT "yo_bg=%s\n",$webdata{'yo_bg'}) ; 
printf(OUT "width=%s\n",$webdata{'width'}) ; 
printf(OUT "height=%s\n",$webdata{'height'}) ; 

printf(OUT "line_width=%s\n",$webdata{'line_width'}) ; 
printf(OUT "cellpadding=%s\n",$webdata{'cellpadding'}) ; 
printf(OUT "border=%s\n",$webdata{'border'}) ; 
printf(OUT "out_line_width=%s\n",$webdata{'out_line_width'}) ; 
printf(OUT "bgcolor=%s\n",$webdata{'bgcolor'}) ; 
printf(OUT "cursor_bg=%s\n",$webdata{'cursor_bg'}) ; 

close(OUT) ;

}



sub display_cfg {
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
<td class="ttl">*** カスタマイズ ***</td>
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
<tbody>
<tr>
<td>
<form method="POST" action="sch_cus.pl">
<table border="0"><tr><td>
線の色:</td><td>
<input size="10" type="text" name="line_color" value="$line_color"></td></tr>
<tr><td>
通常の日の背景色：</td><td>
<input size="10" type="text" name="normal_bg" value="$normal_bg"></td></tr>
<tr><td>
休日の背景色：</td><td>
<input size="10" type="text" name="holiday_bg" value="$ho_bg"></td></tr>
<tr><td>
今日の背景色：</td><td>
<input size="10" type="text" name="today_bg" value="$today_bg"></td></tr>
<tr><td>
月外の日の背景色：</td><td>
<input size="10" type="text" name="other_bg" value="$ot_bg"></td></tr>
<tr><td>
曜日の背景色：</td><td>
<input size="10" type="text" name="yo_bg" value="$yo_bg"></td></tr>
<tr><td>
カレンダーの幅：</td><td>
<input size="10" type="text" name="width" value="$width"></td></tr>
<tr><td>
カレンダーの高さ：</td><td>
<input size="10" type="text" name="height" value="$height"></td></tr>
<tr><td>
線の幅：</td><td>
<input size="10" type="text" name="line_width" value="$line_width"></td></tr>
<tr><td>
セル内余白：</td><td>
<input size="10" type="text" name="cellpadding" value="$cellpadding"></td></tr>
<tr><td>
線のボーダー：</td><td>
<input size="10" type="text" name="border" value="$border"></td></tr>
<tr><td>
外枠 線の幅：</td><td>
<input size="10" type="text" name="out_line_width" value="$out_line_width"></td></tr>
<tr><td>
背景色：</td><td>
<input size="10" type="text" name="bgcolor" value="$bgcolor"></td></tr>
<tr><td>
カー\ソ\ル背景色：</td><td>
<input size="10" type="text" name="cursor_bg" value="$cursor_bg"></td></tr>


</table>
<br>
<input type="submit" name="cfg_ok" value="登録"> &nbsp; &nbsp; 
<input type="hidden" name="ctype" value="$ctype"> 
<a href=./sch_setup.pl>戻る<a/>
</form>
</td>
</tr>
</tbody>
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


sub read_cfg {
local($xx,@key) ;

open (IN,"schcfg.txt");
while ($xx = <IN>) { 
    if ( substr($xx,0,1) eq "#" ) { next ; }  # コメント行
    @key = split("=",$xx ) ;
    chomp($key[1]) ;

    if ( $key[0] eq "line_color" ) { $line_color =  $key[1] } ; 
    if ( $key[0] eq "normal_bg" )  { $normal_bg =  $key[1] } ; 
    if ( $key[0] eq "today_bg" )   { $today_bg =  $key[1] } ; 
    if ( $key[0] eq "holiday_bg" ) { $ho_bg =  $key[1] } ; 
    if ( $key[0] eq "other_bg" )   { $ot_bg =  $key[1] } ; 
    if ( $key[0] eq "yo_bg" )      { $yo_bg =  $key[1] } ; 
    if ( $key[0] eq "width" )      { $width =  $key[1] } ; 
    if ( $key[0] eq "height" )     { $height =  $key[1] } ; 
    if ( $key[0] eq "line_width" ) { $line_width =  $key[1] } ; 
    if ( $key[0] eq "cellpadding" ){ $cellpadding =  $key[1] } ; 
    if ( $key[0] eq "border" )     { $border =  $key[1] } ; 
    if ( $key[0] eq "out_line_width" )     { $out_line_width =  $key[1] } ; 
    if ( $key[0] eq "bgcolor" )    { $bgcolor =  $key[1] } ; 
    if ( $key[0] eq "cursor_bg" )  { $cursor_bg =  $key[1] } ; 

}
close(IN); 

}

