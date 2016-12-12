#!/usr/local/bin/perl

# schdate   スケジュール日付 yyyymmdd
# schdate2  スケジュール終了日付 yyyymmdd
# schrep    繰り返し
# schadj    調整
# schfnt    フォント情報
# schrank   ランク
# schcate   カテゴリ
# schopt    オプション
# schitem   内容

# mode 0 .. スケジュール表示  1 .. 新規入力画面  2 .. 編集画面 
#      3 .. カスタマイズ画面  4 .. 日背景色      5 .. 表示ランク変更
# ctype 0 .. カレンダー型  1 .. 縦型2ヶ月表示  2 .. 縦型3ヶ月表示
#       3 .. 年間カレンダー  4 .. データ一覧   5 .. 週間  6 .. モバイル

require "cgi-lib.pl";

local($i,$j,$k,$ho,$tt) ; 

$version = "1.38" ; 


@monthday = ('31','28','31','30','31','30','31','31','30','31','30','31');
@wkname = ('日','月','火','水','木','金','土') ;
@cname = ("","#ff0000","#008740","#0000ff","#ffff00","#800080","#ff00ff","#00ffff","#ec9800","#ffffff","#000000" ) ; 
@cname2 = ("","赤","緑","青","黄","紫","シアン","水","橙","白","黒" ) ; 
@fixed_item = ("会議","休暇") ; 


                    # 曜日タイトル背景色(日～土)
@youbi_ttl_bgcolor = ("#ffd8dd","#e8edff","#ffefdb","#fffcdd","#e2ffd3","#e2fff9","#dde8ff" ) ; 
                    # 曜日タイトル背景色(1月～12月)  ミニカレンダー
@youbi_ttl_bgcolor_mini = ("","#ffd6e0","#ffd8c9","#ffe5c9","#fff7d1","#f4ffc4","#e5ffbf","#ddffc6","#c9ffc6","#d8ffef","#c6f7ff","#ceddff","#e5dbff");  

                    # 曜日タイトル文字色(日～土)
@youbi_ttl_color = ("#ff0000","#000000","#000000","#000000","#000000","#000000","#0000ff" ) ; 

                    # 曜日背景色(日～土)
@youbi_bgcolor = ("#ffd8dd","#ffffff","#ffffff","#ffffff","#ffffff","#ffffff","#dde8ff" ) ; 


@category = ("","発売日","誕生日") ; 
$ncate = 2  ; 

#open (DDD,"> debug.txt");
#close(DDD) ;

$start_year   = 2012    ;   # 開始年
$end_year     = 2020    ;   # 終了年
$line_color = "#0095ff" ;   # 線の色
$normal_bg =  "#ffffff" ;   # 通常のセル背景色
$ho_bg =      "#fed0e0" ;   # 休日のセル背景色
$ot_bg =      "#dcdcdc" ;   # 月外のセル背景色
$yo_bg =      "#fff200" ;   # 曜日のセル背景色      廃止
$yo_bg_style = 1        ;   # 曜日のセル背景色スタイル 廃止
                            # 0 .. $yo_bg を使用 1.. グラデーション(mini) 
$today_bg =   "#cbffff" ;   # 今日のセル背景色
$sat_bg =     "#e8f2f9" ;   # 土曜日のセル背景色    廃止
$ho_num_cl =      "#ff0000" ;   # 休日の日付の色
$sat_num_cl =     "#0000ff" ;   # 土曜日の日付の色
$normal_num_cl =  "#000000" ;   # 通常の日付の色    廃止
$ho_num_bg =      "#f9ff91" ;   # 休日の日付の背景色 
$sat_num_bg =     "#f9ff91" ;   # 土曜日の日付の背景色
$normal_num_bg =  "#f9ff91" ;   # 通常の日付の背景色
$pri_ho_bg =      "#fcaac9" ;   # 私休日のセル背景色
 

$line_width =  1    ;       # 線の幅
$cellpadding = 2   ;        # セル内余白
$border =      0        ;   # 線のボーダー
$out_line_width = 1    ;    # 外枠 線の幅
$bgcolor =    "#ffffff" ;   # カレンダー外、背景色
$bgimage =    "http://homepage3.nifty.com/supika_star/schwall.gif" ;          # カレンダー外、背景画像

$cursor_bg =  "#ccffcc" ;   # カーソルがあるセルの背景色

$width = 120 ;              # カレンダー項目の幅
$height= 70 ;               # カレンダー項目の高さ
$align = "left" ; 
$valign = "top" ;
$start_wk = 1   ;           # 開始曜日  1 .. 月曜日
$schlen = 99     ;          # 月スケジュール 1項目の長さ
$max_itemcnt = 5 ;          # カレンダーに表示する1日の項目最大数
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
$fmt_nm_bgimage ="<td bgcolor=%s background=\"%s\" align=%s valign=%s class=sc onClick=\"add(%d,%d)\">%s</td>\n" ; 

$fmt_menu="<a href=\"sch.cgi?ctype=%d&yy=%d&mm=%d\">%s</a> \n" ; 


$mode = 0 ; 
$ctype = 0 ; 

&read_cfg ;
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
$edit_ng = $webdata{'edit_ng'} ; 
$add_ng = $webdata{'add_ng'} ; 
$day_bgcolor_add = $webdata{'day_bgcolor_add'} ; 
$cur_rank = $webdata{'cur_rank'} ; 


if ( $cur_rank eq "" ) { $cur_rank = 2 ; } 

open(DBG,">> debug.txt" ) ;
printf(DBG  "cur_rank = %s\n",$cur_rank) ; 
close(DBG) ;


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

&get_holiday ; 
&read_schdata ; 
&read_fixed_item ; 


################### test

#$ctype = 3 ; 

#&display_week ; 
#exit ; 

#open(DBG,"> debug.txt" ) ;
#printf(DBG  "edit_ng = %s\n",$edit_ng) ; 
#close(DBG) ;

###################



if ( $mode == 1  )  {   #  新規入力画面
    &display_add($key) ; 
    exit ; 
}
if ( $mode == 2  )  {   #  編集力画面
    &display_edit($key) ; 
    exit ; 
}

if ( $mode == 4  )  {   #  日背景色設定画面
    &day_bgcolor ; 
    exit ; 
}

if ( $add_ok ne "" ) {  #  item追加処理
    &edit_data(0)  ;
    &display  ;
    exit ;
}

if ( $edit_ok ne "" ) {  #  item修正処理
    &edit_data(1)  ;
    &display  ;
    exit ;
}

if ( $edit_del ne "" ) {  # item削除処理
    &delete_data  ;
    &display  ;
    exit ;
}

if ( $edit_ng eq "キャンセル" ) { #キャンセル処理
    $cur = $webdata{'cur'} ;    
    $cur_yy = int($cur / 100) ; 
    $cur_mm = $cur % 100 ; 
    &display  ;
    exit ;
}

if ( $cfg_ok ne ""  )  {   #  カスタマイズ処理
    &edit_cfg ; 
    &read_cfg ;
    &display  ;
    exit ; 
}

if ( $day_bgcolor_add eq "追加" ) {
    &add_day_bgcolor ; 
}

#printf(DBG  "display\n") ; 
#close(DBG) ;

&display ;
exit ; 

#    週間表示
sub display_week {
local($i,$j,$x,$cyy,$cmm,$cdd,$bg,$dmy,$key,$today_key,$ycl) ; 
#   week_yy  週間表示の最初の日を持つデータ


    $week_yy = $webdata{'yy'} ; 
    $week_mm = $webdata{'mm'} ; 
    $week_dd = $webdata{'wdd'} ; 

    if ( $week_dd == 0 ) {
        ($week_yy,$week_mm,$week_dd) =  &week_start_day  ;
    }
    $today_key = $today_yy * 10000 + $today_mm * 100 +  $today_dd ;
    
    &header    ;
    &menu ;
    &navi_week ;

    printf ("<table class=list bgcolor=%s cellspacing=%s cellpadding=0 onMouseOver=\"overCal(event)\" onMouseOut=\"outCal(event)\">\n",$line_color,$out_line_width) ; 
    printf("<tr><td>") ; 
    printf("<table cellspacing=1 border=0 cellpadding=1 class=list_style>\n") ;
    
    $cyy = $week_yy ;  $cmm = $week_mm ; $cdd = $week_dd ;

    &sch_analize($cyy,$cmm,$cdd,7) ; 

    for ($i = 0 ; $i <= 6 ; $i++ ) {
        $j = $i + $start_wk ; 
        if ( $j >= 7 ) { $j = $j - 7 ; } 
        $x = $wkname[$j]  ; 
        $ycl = $youbi_ttl_color[$j] ;
        ($dmy,$dmy,$bg) = &daynumber_color($cyy,$cmm,$cdd) ; 
        $key = $cyy * 10000 + $cmm * 100 + $cdd ; 
        if ( $key == $today_key ) { #  今日
             $bg = $today_bg ; 
        }

        printf("<tr><td bgcolor=%s height=80>\n",$bg ) ;
        printf("<font color=%s>%d/%d</font></td>",$ycl,$cmm,$cdd) ; 
        printf("<td bgcolor=%s ><font color=%s>%s</font></td><td class=sc bgcolor=#ffffff width=200 valign=top onClick=\"add(%d,5)\">%s</td></tr>\n",$bg,$ycl,$x,$key,$table[$i+1]) ; 
        ($cyy,$cmm,$cdd) = &next_day($cyy,$cmm,$cdd) ; 
    }
    printf("</table></td></tr></table></body></html>\n" ) ;

}

# 週の移動
sub navi_week {
local($i,$j,$x,$cyy,$cmm,$cdd,$bg,$dmy,$key,$x_yy,$x_mm,$x_dd) ; 

    $fmt_week = "<a href=\"sch.cgi?ctype=5&yy=%d&mm=%d&wdd=%d\">%s</a> "  ; 

    ($x_yy,$x_mm,$x_dd) = &calc_ndays($week_yy,$week_mm,$week_dd,14,1) ; 
    printf($fmt_week,$x_yy,$x_mm,$x_dd,"2週前") ; 
    ($x_yy,$x_mm,$x_dd) = &calc_ndays($week_yy,$week_mm,$week_dd,7,1) ; 
    printf($fmt_week,$x_yy,$x_mm,$x_dd,"前週") ; 
    printf($fmt_week,$today_yy,$today_mm,0,"今週") ; 
    ($x_yy,$x_mm,$x_dd) = &calc_ndays($week_yy,$week_mm,$week_dd,7,0) ; 
    printf($fmt_week,$x_yy,$x_mm,$x_dd,"次週") ; 
    ($x_yy,$x_mm,$x_dd) = &calc_ndays($week_yy,$week_mm,$week_dd,14,0) ; 
    printf($fmt_week,$x_yy,$x_mm,$x_dd,"2週後") ; 
}

#   ある日からn日前/後の日付を求める
#   引数  0  年  1 月  2 日  3  日数  4  0の時+  1 の時-
#   返却値  計算結果  0  年  1 月  2 日
sub calc_ndays {
local($yy,$mm,$dd,$endday,$nday,$flg) ; 

    ($yy,$mm,$dd,$nday,$flg) = @_ ; 
    if ( $flg == 0 ) {  #加算
        $endday = &getgetumatu($yy,$mm);    
        $dd = $dd + $nday ; 
        if ( $dd <= $endday ) { return($yy,$mm,$dd) ;  }
        ($yy,$mm) = &next_yymm($yy,$mm) ; 
        $dd =  $dd - $endday; 
        return($yy,$mm,$dd) ;
    }
    else {  #減算
        $dd = $dd - $nday ; 
        if ( $dd >= 1 ) { return($yy,$mm,$dd) ; } 
        ($yy,$mm) = &prev_yymm($yy,$mm) ; 
        $endday = &getgetumatu($yy,$mm);    
        $dd = $endday  + $dd ; 
        return($yy,$mm,$dd) ;
    }
    
}


#   週間表示の最初の日を決定する
#   返却値   週間表示の最初の日の年、月、日
sub week_start_day {
local($i,$j,$cyy,$cmm,$cdd,$you,$endday,$prev_start_day) ; 


    if ( $cur_yy == $today_yy &&  $cur_mm == $today_mm ) { # 今月の場合
        $you = &day_week($cur_yy,$cur_mm,$today_dd); 
        if ( $you == $start_wk ) {
            return($cur_yy,$cur_mm,$today_dd) ; 
        }
        $i = $you - $start_wk ;  #週頭まで何日戻すか
        if ( $i < 0 ) { $i = $i + 7 ; } 
        ($cyy,$cmm,$cdd) = &calc_ndays($cur_yy,$cur_mm,$today_dd,$i,1) ; 
        return($cyy,$cmm,$cdd) ; 
    }
    $you = &day_week($cur_yy,$cur_mm,1);  # 1日の曜日

    ($cyy,$cmm) = &prev_yymm($cur_yy,$cur_mm) ; # 前月
    $prev_start_day = &prev_mon_day($cyy,$cmm,$you) ; # 前月最初の日 
    if ( $prev_start_day == 0 ) {
        return($cur_yy,$cur_mm,1); 
    }
    else {
        return($cyy,$cmm,$prev_start_day); 
    }

}

# データ一覧
sub list_data {
local($xx) ; 

printf("Content-type: text/html\n\n" ) ; 

open (IN,"schdata.txt");
$i = 0 ; 
while ($xx = <IN>) { 
    printf("%s<br>\n",$xx ) ; 
}
close(IN); 

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

sub display  {

if ( $ctype == 0 ) { &calender ; } 
if ( $ctype == 1 ) { &display_list(2)  ; } 
if ( $ctype == 2 ) { &display_list(3) ; } 
if ( $ctype == 3 ) { &year_calender ; } 
if ( $ctype == 4 ) { &list_data ; } 
if ( $ctype == 5 ) { &display_week ; } 
if ( $ctype == 6 ) { &display_mobile ; } 
}

#    モバイル用 表示
sub display_mobile {
local($i,$j,$cyy,$cmm,$cdd,$wk,$save_rank) ; 

$save_rank = $cur_rank ; 
$cur_rank = 1 ; 
&sch_analize($today_yy,$today_mm,$today_dd,100) ; 
$cur_rank  = $save_rank ; 

$cyy = $today_yy ; 
$cmm = $today_mm ; 
$cdd = $today_dd ; 

$wk = &day_week($cyy,$cmm,$cdd);  # 


print << "EOF";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Style-Type" content="text/css">
<meta name="viewport" content="width=device-width,user-scalable=yes, initial-scale=1.0" />
<title>sch</title>
</head>
EOF

for($i = 1 ; $i <= 100 ; $i++ ) {  # 100日先まで表示

    if ( $table[$i] ne "" ) {
        if ( $wk == 0 ) {
            printf("<font color=red>%02d/%02d(%s)</font> %s<br>\n",$cmm,$cdd,$wkname[$wk],$table[$i]) ; 
        }
        else {
            if ( $wk == 6 ) {
                printf("<font color=blue>%02d/%02d(%s)</font> %s<br>\n",$cmm,$cdd,$wkname[$wk],$table[$i]) ; 
            }
            else{
                printf("%02d/%02d(%s) %s<br>\n",$cmm,$cdd,$wkname[$wk],$table[$i]) ; 
            }
        }
    }
    ($cyy,$cmm,$cdd) = &next_day($cyy,$cmm,$cdd) ; 
    $wk++ ; 
    if (  $wk == 7 ) { $wk = 0 ;  }
}
printf("</html>\n") ; 
}


sub year_calender {

    &year_calender_body($cur_yy,$cur_mm) ; 
}

sub year_calender_body {
local($i,$cyy,$cmm,$nyy,$nmm,$pyy,$pmm) ; 

$cyy = $_[0] ; 
$cmm = $_[1] ; 

&header;

printf("**** sch **** Ver. %s <br>\n",$version ) ; 

&menu ;

($nyy,$nmm) = next_yymm($cyy,$cmm) ; 
($pyy,$pmm) = prev_yymm($cyy,$cmm) ; 
printf("<a href=\"sch.cgi?ctype=3&yy=%d&mm=%d\">前年</a>\n",$cyy-1,$cmm ) ; 
printf("<a href=\"sch.cgi?ctype=3&yy=%d&mm=1\">年初</a>\n",$cyy ) ; 
printf("<a href=\"sch.cgi?ctype=3&yy=%d&mm=%d\">前月</a>\n",$pyy,$pmm ) ; 
printf("<a href=\"sch.cgi?ctype=3&yy=%d&mm=%d\">今月</a>\n",$today_yy,$today_mm) ; 
printf("<a href=\"sch.cgi?ctype=3&yy=%d&mm=%d\">来月</a>\n",$nyy,$nmm ) ; 
printf("<a href=\"sch.cgi?ctype=3&yy=%d&mm=%d\">来年</a>\n",$cyy+1,$cmm ) ; 

printf("<table cellpadding=5> <tr>\n") ;
for ($i = 1 ; $i <= 12 ; $i++ ) {
    printf("<td valign=top >\n") ;
    &cal_mini($cyy,$cmm) ;
    if ( $i % 4 == 0 ) {
        printf("</td></tr><tr>\n") ; 
    }
    else {
        printf("</td>\n") ; 
    }
    ($cyy,$cmm) = next_yymm($cyy,$cmm) ; 
}
printf("</tr></table>\n</body></html>\n") ;

}


#   カレンダー型の表示
sub calender  {
local($cyy,$cmm) ; 

&header;
printf("**** sch **** Ver. %s <br>\n",$version ) ; 
&menu ;
&make_link ; 

&cal_body(0,0) ; 

printf("<table><tr><td valign=top>\n") ;
($cyy,$cmm) = prev_yymm($cur_yy,$cur_mm) ; 
&cal_mini($cyy,$cmm) ;
printf("</td><td valign=top>\n") ;
&cal_mini($cur_yy,$cur_mm) ;
printf("</td><td valign=top>\n") ;
($cyy,$cmm) = next_yymm($cur_yy,$cur_mm) ; 
&cal_mini($cyy,$cmm) ;

printf("</td></tr></table>\n</body></html>\n") ;
}

sub menu {
#$fmt_menu="<a href=\"sch.cgi?ctype=%d&yy=%d&mm=%d\">%s</a>\n" ; 

printf($fmt_menu,5,$cur_yy,$cur_mm,"週間") ; 
printf($fmt_menu,0,$cur_yy,$cur_mm,"1ヶ月") ; 
printf($fmt_menu,1,$cur_yy,$cur_mm,"2ヶ月") ; 
printf($fmt_menu,2,$cur_yy,$cur_mm,"3ヶ月") ; 
printf($fmt_menu,3,$cur_yy,$cur_mm,"年間") ; 

#printf("<a href=\"sch.cgi?mode=3&ctype=%d\">カスタマイズ</a>   ",$ctype ) ; 
#printf("<a href=\"sch_list.cgi\">データ一覧</a>\n" ) ; 
#printf("<a href=\"sch_item.cgi\">定型項目編集</a>\n" ) ; 
#printf("<a href=\"sch_holi.cgi\">休日設定</a>\n" ) ; 
printf("<b>ランク変更</b><a href=\"sch.cgi?cur_rank=0&yy=%d&mm=%d&ctype=%d\">0</a>\n", $cur_yy,$cur_mm,$ctype) ; 
printf("<a href=\"sch.cgi?cur_rank=1&yy=%d&mm=%d&ctype=%d\">1</a>\n",$cur_yy,$cur_mm,$ctype ) ; 
printf("<a href=\"sch.cgi?cur_rank=2&yy=%d&mm=%d&ctype=%d\">2</a>\n",$cur_yy,$cur_mm,$ctype ) ; 
printf("<b>現在ランク</b> %d\n",$cur_rank ) ; 
printf("<a href=\"sch.cgi?ctype=6\">携帯</a>\n" ) ; 
printf("<a href=\"sch_setup.cgi\"  target=\"_blank\">設定</a>   ") ; 
printf("<a href=\"sch.cgi?mode=4\">日背景色</a>\n" ) ; 

printf("<br>\n") ;

}


#   カレンダー本体
#       引数    $_[0] .... 年(0の時 cur_yy)   $_[1] .... 月
sub cal_body  {
local($yymm,$p,$k, $i,$j,$fmt_dd,$fmt_bg,$cyy,$cmm,$cdd,$key,$today_key,$cnt,$cur_pyy,$cur_pmm,$startday,$endday) ; 
local($ttl_yy,$ttl_mm,$ccs_name) ; 

if ( $_[0] == 0 ) {
    $cyy = $cur_yy ;   $cmm = $cur_mm ; 
}
else {
    $cyy = $_[0] ;   $cmm = $_[1] ; 
}

$ttl_yy = $cyy ;  $ttl_mm = $cmm ; 

$startday = &day_week($cyy,$cmm,1);  # 1日の曜日
$endday = &getgetumatu($cyy,$cmm);   # 月末の日
($cur_pyy,$cur_pmm) = &prev_yymm($cyy,$cmm) ; # 前月
$prev_start_day = &prev_mon_day($cur_pyy,$cur_pmm,$startday) ;  # 前月最初の日 

if ( $prev_start_day == 0 ) {   
    $cdd = 1 ; 
}
else {
    $cyy = $cur_pyy ; $cmm = $cur_pmm ; $cdd = $prev_start_day ; 
}

printf("&nbsp;&nbsp;&nbsp;&nbsp;<b>    %d 年 %d月</b><br>\n",$ttl_yy,$ttl_mm) ; 

if ( $cal_mini_flg == 0 ) {  # 通常カレンダー
	printf("<table border=0 bgcolor=%s cellspacing=%s cellpadding=0 onMouseOver=\"overCal(event)\" onMouseOut=\"outCal(event)\">\n", $line_color,$out_line_width);
	$ccs_name = "main_style" ; 
}
else {                       #  ミニカレンダー
	printf("<table class=minical border=0 bgcolor=%s cellspacing=%s cellpadding=0 onMouseOver=\"overCal(event)\" onMouseOut=\"outCal(event)\">\n", $line_color,$out_line_width);
    $ccs_name = "mini_style" ; 
}
print "<tr><td>\n" ; 

printf("<table cellspacing=%s border=%s cellpadding=%s class=%s>\n",
         $line_width,$border,$cellpadding,$ccs_name) ; 

#    曜日
if ( $cal_mini_flg == 1 ) {
    printf("<tr bgcolor=%s>\n",@youbi_ttl_bgcolor_mini[$ttl_mm]) ; 
}
else {
    printf("<tr>\n") ; 
}
&youbi_header ; 
print "</tr>\n" ; 

if ( $cal_mini_flg == 0 ) { &sch_analize($cyy,$cmm,$cdd,42) ;  }


$today_key = $today_yy * 10000 + $today_mm * 100 +  $today_dd ;
$cnt = 0 ;
for ( $i = 1 ; $i <= 6 ; $i++ ) {
    if ( $cmm !=  $ttl_mm && $i == 6 ) { last ; } 
    printf ("<tr  height=%d>",$ height)  ; 
    for ( $j = 1 ; $j <= 7 ; $j++ ) {
        $cnt++ ; 
        &make_day_item($cyy,$cmm,$cdd,$ttl_mm,$today_key,$cnt) ; 
        ($cyy,$cmm,$cdd) = &next_day($cyy,$cmm,$cdd) ; 
    }
    print "</tr>\n" ; 
}

print <<EOF;
</table>
</td></tr></table>
EOF

}

#    カレンダーの1日枠に入れる情報を作成
#    引数  0 .. 年 1 .. 月  2 .. 日  3 .. タイトル月  4 .. today_key 5 .. cnt
sub make_day_item {
local($i,$j,$cyy,$cmm,$cdd,$key,$tmm,$today_key,$s,$daynumber,$cnt) ; 
local($num_cl,$num_bg,$bg,$s,$bg_image ) ; 

    ($cyy,$cmm,$cdd,$tmm,$today_key,$cnt) = @_ ; 
    $key = $cyy * 10000 + $cmm * 100 + $cdd ; 
    
    if ( $cmm != $tmm ) {  #  月外の日
        if ( $cal_mini_flg == 0 ) { 
        printf ($fmt_nm,$ot_bg,$align,$valign,$key,$ctype,$cdd . $table[$cnt])  ; 
        }
        else {
        printf ($fmt_nm,$ot_bg,$align,$valign,$key,$ctype,$cdd)  ; 
        }
        return ;
    }

    $fmt_dd = "<span class=daynumber>" . $cdd . "</span>" ; 
    ($num_cl,$num_bg,$bg,$bg_image) = &daynumber_color($cyy,$cmm,$cdd) ; 

    if ( $key == $today_key ) { #  今日
         $bg = $today_bg ; 
    }
    if ( $cal_mini_flg == 0 ) { 
        $s = $cdd ; 
        if ( $cdd <= 9 ) { $s = "&nbsp;" . $cdd } ;  
        $daynumber = "<span class=\"daynumber\" style=\"color : " . $num_cl . " ; background-color : " .  $num_bg . "\">" . $s . "</span>" ; 
        $s = $daynumber . $table[$cnt] ; 
    }
    else {       # ミニカレンダー
        $s = "<span style=\"color : " . $num_cl . "\">" . $cdd . "</span>"
    }
    if ( $bg_image eq "" ) { 
        printf($fmt_nm,$bg,$align,$valign,$key,$ctype,$s); 
    }
    else {
        printf($fmt_nm_bgimage,$bg,$bg_image,$align,$valign,$key,$ctype,$s); 
    }

}

#    日の背景色と日付数字のスタイル設定
#      引数     0 .. 年 1 .. 月  2 .. 日
#      返却値  日付文字の色 日付文字の背景色 日付セルの背景色 背景画像URL
sub daynumber_color {
local($num_cl,$num_bg,$bg,$ret,$dbg,$bg_image ) ; 

    $bg_image = "" ;
    $ret = &check_holiday($_[0],$_[1],$_[2]) ; 
    if ( $ret == 1  ) { # 日休日 私休日
        $num_cl = $ho_num_cl ; 
        $num_bg = $ho_num_bg ; 
        $bg = $ho_bg ; 
    }
    elsif ( $ret == 3 ) { # 私休日
        $num_cl = $ho_num_cl ; 
        $num_bg = $ho_num_bg ; 
        $bg = $pri_ho_bg ; 
    }
    elsif ( $ret == 2 ) {         # 土曜日
        $num_cl = $sat_num_cl ; 
        $num_bg = $sat_num_bg ; 
#       $bg = $sat_bg ; 
        $bg = $youbi_bgcolor[6]  ; 
    }
    else {            
        $num_cl = $normal_num_cl ; 
        $num_bg = $normal_num_bg ; 
#        $bg = $normal_bg ;  # 平日
        $bg= $youbi_bgcolor[&day_week($_[0],$_[1],$_[2])] ; 
    }
    
    $dbg = &check_daybgcolor($_[0],$_[1],$_[2]) ;  # 日の背景色

    if ( $dbg ne "" ) {           #  背景色
        if ( substr($dbg,0,1) ne "#" ) {  #  背景画像
            $bg_image = $dbg ;
        }
        else {
            $bg =  $dbg; 
        }
    }
    return($num_cl,$num_bg,$bg,$bg_image) ; 

}


#   ミニカレンダー本体
#       引数  
sub cal_mini  {
local($sv_width,$sv_height,$sv_align)  ;

#   待避
$sv_height = $height ; 
$sv_width = $width ; 
$sv_align = $align ; 

$height = 0 ; 
$width = 0 ;
$align = "right" ; 
$cal_mini_flg = 1 ;

&cal_body($_[0],$_[1]) ;

#  復元
$height = $sv_height  ; 
$width = $sv_width ; 
$align = $sv_align ; 
$cal_mini_flg = 0 ;

return ; 
}

#   縦型表示
#       引数    1 .. 1ヶ月表示   2 ... 2ヶ月表示  3 ... 3ヶ月表示
sub display_list {


&header;
printf("**** sch **** Ver. %s <br>\n",$version ) ; 
&menu ;
&make_link ; 

printf("<table><tr><td align=center valign=top bgcolor=#d8ffba>\n") ; 
if ( $_[0] == 2 ) { 
    &display_list_unit(0) ; 
    printf("</td><td align=center valign=top bgcolor=#d8ffe8>\n") ; 
    &display_list_unit(1) ; 
}
if ( $_[0] == 3 ) { 
    &display_list_unit(0) ; 
    printf("</td><td align=center valign=top bgcolor=#d3ffe2>\n") ; 
    &display_list_unit(1) ; 
    printf("</td><td align=center valign=top bgcolor=#ffd6ff>\n") ; 
    &display_list_unit(2) ; 
}
printf("</td></tr></table>\n</body></html>\n") ; 
}

#   縦型表示  1ヶ月分
#   引数   0 .... 現在の年月    1 .... 次月    -1  .... 先月
sub display_list_unit {
local($i,$j,$cyy,$cmm,$cdd,$key,$wk,$s,$base,$endday,$num_cl,$num_bg) ; 

if ( $_[0] == 0 ) { 
    $cyy = $cur_yy ; $cmm = $cur_mm ; 
}
if ( $_[0] == 1 )  { ($cyy,$cmm) = next_yymm($cur_yy,$cur_mm) ; } # 次月
if ( $_[0] == -1 ) { ($cyy,$cmm) = prev_yymm($cur_yy,$cur_mm) ; }
if ( $_[0] == 2 )  { 
    ($cyy,$cmm) = next_yymm($cur_yy,$cur_mm) ;
    ($cyy,$cmm) = next_yymm($cyy,$cmm) ;
}

$wk = &day_week($cyy,$cmm,1);  # 1日の曜日
$endday = &getgetumatu($cyy,$cmm);   # 月末の日
    $today_key = $today_yy * 10000 + $today_mm * 100 +  $today_dd ;

printf("  %d 年 %d月<br>\n",$cyy,$cmm) ; 
printf("<table class=list bgcolor=%s cellspacing=%s cellpadding=0 onMouseOver=\"overCal(event)\" onMouseOut=\"outCal(event)\">\n", $line_color,$out_line_width);
print "<tr><td>\n" ; 
printf("<table cellspacing=%s border=%s cellpadding=%s class=list_style>\n",
         $line_width,$border,$cellpadding_2month) ; 

#printf("<tr bgcolor=#8cd3db><td align=center >日</td><td align=center >曜</td><td align=center width=200> 予\定 </td></tr>\n") ;

&sch_analize($cyy,$cmm,1,42) ; 

$base = $cyy * 10000 + $cmm * 100 ; 
for($i = 1 ; $i <= $endday ; $i++ ) {
    $key = $base + $i ; 
    ($num_cl,$num_bg,$s) = &daynumber_color($cyy,$cmm,$i) ; 
    if ( $key == $today_key ) { #  今日
         $s = $today_bg ; 
    }
    printf("<tr><td bgcolor=%s ><span style=\"color : %s\">%d</span></td><td bgcolor=%s align=center><span style=\"color : %s\">%s</span></td><td bgcolor=#ffffff class=sc onClick=\"add(%d,%d)\" width=400>%s</td></tr>\n",$s,$num_cl,$i,$s, $youbi_ttl_color[$wk],  $wkname[$wk],$key,$ctype,$table[$i]) ; 
    $wk++ ; 
    if ( $wk == 7 ) { $wk = 0 ; } 
}

printf("</table>\n</td></tr></table>\n")  ; 

}

#   日付データ テスト用
sub test_date_match {
local($ckdate) ;

    &get_holiday ; 
    &read_schdata ; 
$endday = 28;

    $ckdate = 20050214 ;
    print "test_date_match=" . &get_schdata($ckdate) ; 
    
}


#   table データにスケジュールを格納する
#   引数   0  1  2  開始年月日  3  データ数
sub sch_analize {
local($i,$yy,$mm,$dd,$key,$n) ; 

    ($yy,$mm,$dd,$n) = @_ ; 
    for($i = 1 ; $i <= $n ; $i++ ) {  # 最大6行
        $table[$i] = ""  ;  # get_schdata でデータを入れる前にクリア
    }
    
    for($i = 1 ; $i <= $n ; $i++ ) {  # 最大6行
        $key = $yy * 10000 + $mm * 100 + $dd ;
        &get_schdata($key,$i); 
        ($yy,$mm,$dd) = &next_day($yy,$mm,$dd) ; 
    }

}

#  引数  $_[0]   yyyymmdd   $_[1]  調整フラグ
#  引数の日付のスケジュールデータを返す
#  サブ内で grid_data に格納するよう変更
sub get_schdata  {
local($x,$s,$i,$j,$rep,$wd,$ycnt,$endf,$you,$type  ) ; 
local($adjtype,$adjproc,$adjdate,$match,$matchcnt) ; 
    $i = 0 ; 

    $matchcnt = 0 ; 
    for($i = 0 ; $i <= $nsch ; $i++ ) {
        $s = "" ; 
        $match = 0 ;

        if ( $schopt[$i] == 1 ) { next ; }   #  日背景色
        if ( $schrank[$i] > $cur_rank ) { next ; } # ランク以下は省く

                              # 範囲外は除く
        if ( $schdate[$i] > $_[0] || $schdate2[$i] <  $_[0] ) { next ; } 

        $type = substr($schrep[$i],0,1) ; 

        if ( $type == 0  ) {  # 通常
            if ($schdate[$i] == $_[0] ) { $match = 1 ; }

        } elsif ( $type == 1  ) {  # 毎月特定日
            $rep = substr($schrep[$i],1,2) ; 
            if ( $rep == $_[0] % 100 ) { $match = 1 ; }

        } elsif ( $type == 2  ) {  # 毎年特定日
            $rep = substr($schrep[$i],1,4) ; 
            if ( $rep == $_[0] % 10000 ) { $match = 1 ; }

        } elsif ( $type  == 3  ) {  # 特定曜日
            $wd = &day_week(&yy_mask($_[0]),&mm_mask($_[0]),&dd_mask($_[0])) ; 
#            print "wd= " . $wd . "\n" ; 
#            printf("schrep %s len %d  \n",$schrep[$i],length($schrep[$i]) ) ; 

            for ($j=1 ; $j <= length($schrep[$i]) - 1 ; $j++ ) {
                $rep = substr($schrep[$i],$j,1) ;   # 指定曜日
#                printf("rep %d \n",$rep ) ; 
                if ( $rep == $wd ) { $match = 1 ; }
            }
        } elsif ( $type == 4  ) {  # 第n曜日
            $wd = &day_week(&yy_mask($_[0]),&mm_mask($_[0]),&dd_mask($_[0])) ; 
            ($ycnt,$endf) = &youbi_cnt($_[0]) ; 
#            printf(" ycnt endf wd %d  %d  %d \n",$ycnt,$endf,$wd ) ; 
            
            $you = substr($schrep[$i],1,1) ;     # 指定曜日
            for ($j=2 ; $j <= length($schrep[$i]) - 1 ; $j++ ) {
                $rep = substr($schrep[$i],$j,1) ; 
#                printf("you %d rep %d \n",$you, $rep ) ; 
                if ( $you == $wd ) {             # 曜日が一致した
                    if ( $rep == 9 ) {           # 最終週
                        if ( $endf == 1 ) { $match = 1 ; }
                    }
                    else {
                        if ( $rep == $ycnt ) { $match = 1 ; }
                    }
                }
            }
        }
        
        if ( $match == 1 ) { 
            $s = &day_format($schitem[$i],$i) ; 
            $matchcnt++ ; 
        }

        $adj = $_[1] ; 
        if ( $s ne "" ) { $adj = &adjustment($i,$_[0],$_[1]) ;  }

        # 最大数を超えたら終わり
        if ( $ctype == 0 && $matchcnt > $max_itemcnt ) { 
            $table[$adj] = $table[$adj] . " ..."  ; 
            return ; 
            # 調整によって日がずれた時に$max_itemcnt以上書いてしまう
            # 問題あり
        } 
        else {
            if ( $adj != -1 ) { $table[$adj] = $table[$adj] . $s ;  }
        }
        

#        printf("adj %d table %s \n",$adj,$table[$adj]  ) ; 
        
    }

}

#    調整処理
#    $_[0] ... データのindex  $_[1] ... 基準となる日付 $_[2] tableのindex
#    返却値  調整後のtableのindex  -1 は無効
sub adjustment {
local($i,$j,$adjtype,$adjproc,$adjdate) ;
    $i = $_[0] ; 
    $adjdate = $_[1] ; 
    $adjtype = substr($schadj[$i],0,1) ; 
    $adjproc = substr($schadj[$i],1,1) ; 

    if ( &check_adj_cond($adjtype,$adjdate) == 0 ) { #条件に一致しない
        return($_[2]) ;  # 変化がないのでtableのindexをそのまま返す 
    }
    if ( $adjproc == 1 ) {  #  前にずらす
        $j = 1 ; 
        while ( $_[2]-$j >= 1 ) { 
            $adjdate = &prev_day2($adjdate) ; 
            if ( &check_adj_cond($adjtype,$adjdate) == 0 ) {
                return($_[2]-$j) ; 
            }
            $j++ ;
        }
        return(-1) ;   #  範囲外になった
    }
    if ( $adjproc == 2 ) {  #  後ろにずらす
        # 未サポート
    }
    if ( $adjproc == 3 ) {  #  無効
        return(-1) ; 
    }

}

#    調整の条件にマッチするかチェックする
#    $_[0]  調整タイプ    $_[1]  日付
#    返却値   マッチしたら 1 を返す
sub check_adj_cond {
    if ( $_[0] == 1 ) {   # 休日を変更(土日祝、私)
        if (&check_holiday(&yy_mask($_[1]),&mm_mask($_[1]),&dd_mask($_[1])) 
               != 0 ) {
            return(1) ; 
        }
    }
    if ( $_[0] == 2 ) {   # 日曜日、祝日を変更
        if (&check_holiday(&yy_mask($_[1]),&mm_mask($_[1]),&dd_mask($_[1])) 
               == 1 ) {
            return(1) ; 
        }
    }
    return(0) ; 
}

#    _[0] ... schitem   _[1] ...  key 
sub day_format {
local($s,$c,$bc,$sty,$cur) ; 

#   $s = $s . "<br>" . $_[0] ; 

    if ( $ctype ==6 ) {   # モバイル
        return($_[0] . " ") ;
    }

    
    $cur = $cur_yy * 100 + $cur_mm  ;
    $sty = "" ; 
    ($c,$bc) = &font_analize($_[1]) ; 
    if ( $c ne "" )   { $sty = "color:" . $c . ";" ; } 
    if ( $bc ne "" )  { $sty = $sty . "background-color : " . $bc . ";" ; } 
    if ( $sty ne "" ) { $sty = " style=\"" . $sty . "\"" ; }
        
    $s = "<a href=sch.cgi?mode=2&ctype=" . $ctype . "&cur=" . $cur . "&key=" . $_[1] . $sty . ">" . substr($_[0],0,$schlen)  . "</a>" . " " ; 
    if ( $ctype == 0 || $ctype == 5) {   
        $s = "<br>" . $s ;  # カレンダー型表示
    }

    return($s) ; 
}

#        フォント情報の解析
sub font_analize {
local(@font) ; 

    @font = split("," , $schfnt[$_[0]] ) ; 
    
#    if ( $font[0] eq "" ) { $font[0] = "#000000" ;   }
    return($font[0],$font[1]) ;   #  カラー 背景色

}
sub prev_yymm { 
local($yy,$mm) ; 
    if ( $_[1] == 1 ) { 
        $mm = 12 ;  $yy = $_[0] - 1 ; 
    }
    else {
        $mm =  $_[1] - 1 ; $yy = $_[0]  ; 
    }
    return($yy,$mm ) ;
}

sub next_yymm { 
local($yy,$mm) ; 
    if ( $_[1] == 12 ) { 
        $mm = 1 ;  $yy = $_[0] + 1 ; 
    }
    else {
        $mm =  $_[1] + 1 ; $yy = $_[0]  ; 
    }
    return($yy,$mm ) ;
}

#   カレンダー1行目の開始日を返す
#       0 の場合はちょうど当月から始まる
#       引数  _[0] .. 前月の年  _[1] .. 前月の月   _[2]  当月の開始曜日
sub prev_mon_day { 
local($e,$i) ; 
    if ( $_[2] == $start_wk  ) { return(0) ; }  #開始曜日と一致したら
    $e = &getgetumatu($_[0],$_[1]);   # 前月月末の日
    $i = $_[2] - $start_wk - 1 ; 
    if ( $i < 0 )  { $i = $i + 7 ;  } 
    $e = $e - $i ; 
    return($e) ; 

}

#  引数 yyyy mm dd の次の日を返す
sub next_day {
local($yy,$mm,$dd) ; 

    $dd = $_[2] + 1 ; 
    if ( $dd > &getgetumatu($_[0],$_[1]) ) {
        ($yy,$mm) = &next_yymm($_[0],$_[1]) ;
        $dd = 1 ; 
    }
    else {
        $yy = $_[0] ;  $mm = $_[1] ; 
    }
    return($yy,$mm,$dd); 
}


#  引数 yyyy mm dd の前の日を返す
sub prev_day {
local($yy,$mm,$dd) ; 

    $dd = $_[2] - 1 ; 
    if ( $dd == 0 ) {
        ($yy,$mm) = &prev_yymm($_[0],$_[1]) ;
        $dd = &getgetumatu($yy,$mm) ; 
    }
    else {
        $yy = $_[0] ;  $mm = $_[1] ; 
    }
    return($yy,$mm,$dd); 
}

#  引数 yyyymmdd の前の日を yyyymmdd 形式で返す
sub prev_day2 {
local($yy,$mm,$dd) ; 

    $yy = &yy_mask($_[0]) ; $mm = &mm_mask($_[0]) ; $dd = &dd_mask($_[0]) ;
    ($yy,$mm,$dd) = &prev_day($yy,$mm,$dd) ; 
    return($yy*10000+$mm*100+$dd); 
}


#    第何週かを返す
#    $_[0]  日付  yyyymmdd
sub youbi_cnt {
local($i,$ew,$yy,$mm,$dd,$endday) ;
#    printf("youbi_cnt endday  %d \n",$endday )  ;

    $yy = &yy_mask($_[0]) ; $mm = &mm_mask($_[0]) ; $dd = &dd_mask($_[0]) ;
    $endday = &getgetumatu($yy,$mm) ; 

    $ew = 0 ; 
    $i = int(($dd-1) / 7 ) + 1 ; 
    if ( $dd > ($endday - 7) ) {  $ew = 1 ; } # 最終週 
#    printf("youbi_cnt  i  %d \n",$i )  ;
    return($i,$ew ) ; 
}


sub yy_mask {
    return( int($_[0] / 10000 )) ; 
}
sub mm_mask {
    return( int(($_[0] / 100)) % 100 ) ; 
}
sub dd_mask {
    return( $_[0] % 100 ) ; 
}

#                   スケジュールデータの読み込み
sub read_schdata {
local($i,$xx,@key,@sdata,@ymd,$s) ; 

open (IN,"schdata.txt");
$i = 0 ; 
while ($xx = <IN>) { 
    @key = split("	",$xx ) ;
    @sdata = split(";" , $key[0] ) ; 

    @ymd = split("/",@sdata[0]) ; 
    if ( $ymd[0] eq "" ) {
        $schdate[$i] = 0 ; 
    }
    else {
        $schdate[$i] = $ymd[0] * 10000 + $ymd[1]  * 100 + $ymd[2] ; 
    }

    @ymd = split("/",@sdata[1]) ; 
    if ( $ymd[0] eq "" ) {
        $schdate2[$i] = 99991231 ; 
    }
    else {
        $schdate2[$i] = $ymd[0] * 10000 + $ymd[1]  * 100 + $ymd[2] ; 
    }

    $schrep[$i] = @sdata[2] ; 
    $schadj[$i] = @sdata[3] ; 
    $schfnt[$i] = @sdata[4] ; 
    $schrank[$i] = @sdata[5] ; 
    $schcate[$i] = @sdata[6] ; 
    $schopt[$i] = @sdata[7] ; 
    if ( $schrank[$i] eq "" ) { $schrank[$i] = 0 ; }  # 互換のため
    if ( $schcate[$i] eq "" ) { $schcate[$i] = 0 ; }  # 互換のため
    
#    printf(" schfnt = %s \n",$schfnt[$i]) ; 


    $s =$key[1] ; 
    $s =~ s/\n// ;
    $s =~ s/\r// ; 
    $schitem[$i] = $s  ; 
    $i++;
}
$nsch = $i - 1 ;   # データの数
close(IN); 
}
                # 定型行事の読み込み
sub read_fixed_item {
local($i,$xx) ; 

    open (IN,"item.txt");
    $i = 0 ; 
    while ($xx = <IN>) {
        $fixed_item[$i] = $xx ; 
        $i++ ; 
    }
    close(IN); 
}

                # item の追加 編集
sub edit_data {
local($yy,$mm,$dd,$yy2,$mm2,$dd2,$x,$x2,$rep,$attr,@ckbox,$p) ;
local($chcl,$chbc,$cur,$wfnt1,$wfnt2,$cp) ; 

$yy   = $webdata{'yy1'} ;    
$mm   = $webdata{'mm1'} ;    
$dd   = $webdata{'dd1'} ;    
$yy2  = $webdata{'yy2'} ;    
$mm2  = $webdata{'mm2'} ;    
$dd2  = $webdata{'dd2'} ;    
$rep  = $webdata{'rep'} ;    
$chcl = $webdata{'chcl'} ;    
$chbc = $webdata{'chbc'} ;    


if ( $_[0] == 0 ) {   #  追加

    $nsch++ ;
    $p = $nsch ; 
    $cur_yy = $webdata{'cur_yy'} ;    
    $cur_mm = $webdata{'cur_mm'} ;    
}
else {                # 編集
    $p = $webdata{'key'} ;    
    $cur = $webdata{'cur'} ;    
    $cur_yy = int($cur / 100) ; 
    $cur_mm = $cur % 100 ; 
}


$schitem[$p] = $webdata{'item'} ; 

if ($schitem[$p] eq "" ) {$schitem[$p] =  "***"} # 項目がない場合

#############
#$d="20050228" ; 
#$schitem[$nsch] = "test0228" ; 
#############

$schdate[$p] = $yy * 10000 + $mm * 100 + $dd ; 

if (  $yy2 == 0 ) { $schdate2[$p] = 99991231 ; } 
else {
    $schdate2[$p] = $yy2 * 10000 + $mm2 * 100 + $dd2 ; 
}

                           # 色、背景色の設定
$wfnt1 = "" ; 
$wfnt2 = "" ; 
if ( $chcl != 0 ) { $wfnt1 = $cname[$chcl] ; } ; 
if ( $chbc != 0 ) { $wfnt2 = $cname[$chbc] ; } ; 

$schfnt[$p] = $wfnt1 . "," . $wfnt2 ; 



if ( $rep eq "rep0" ) { $attr = "0" } ; 
if ( $rep eq "rep1" ) {    # 毎週特定曜日
    $attr = "3" ;
#    @ckbox = $qqq -> param('repweek') ;  
    @ckbox = &SplitParam($webdata{'repweek'});
    foreach $x (@ckbox) {
        $attr = $attr . $x  ;
    }
} 

if ( $rep eq "rep2" ) {   # 毎月特定日
    $attr = "1" ; 
    $x = $webdata{'repdd'} ; 
    $attr = $attr . substr("0" . $x , -2 ,2 )  ; 
} 

if ( $rep eq "rep3" ) {   # 第n曜
    $attr = "4" ;
    $x = $webdata{'repww'} ;    
    $attr = $attr . $x  ;
    
    @ckbox = $webdata{'repcnt'} ;    
    foreach $x (@ckbox) {
        $attr = $attr . $x  ;
    }
} 

if ( $rep eq "rep4" ) {   # 毎年特定日
    $attr = "2" ;
    $x = $webdata{'rep4mm'} ; 
    $attr = $attr . substr("0" . $x , -2 , 2 )   ;
    $x = $webdata{'rep4dd'} ; 
    $attr = $attr . substr("0" . $x , -2 , 2 )   ;
} 

$schrep[$p] = $attr ; 

# 調整
$x = $webdata{'adjcond'} ; 
$schadj[$p]  = "" ;
if ( $x ne "0" ) {
    $schadj[$p] = $x . $webdata{'adj'}; 
}

# ランク
$x = $webdata{'rank'} ; 
$schrank[$p] = $webdata{'rank'} ;  
$schcate[$p] = $webdata{'cate'};  


&write_schdata ;
}

sub write_schdata {
local($i) ;

open (OUT,"> schdata.txt");
for ( $i = 0 ; $i <= $nsch ; $i++ ) {
    &write_schdata_line($i) ; 
}

close(OUT); 
}

sub write_schdata_line {
local($i,$x,$x2) ;

$x = &num_to_date($schdate[$_[0]]) ; 
if ( $schdate2[$_[0]] eq "99991231" ) { 
    $x2 = "" ; 
}
else {
    $x2 = &num_to_date($schdate2[$_[0]]) ; 
}
printf(OUT "%s;%s;%s;%s;%s;%s;%s;%s;\t%s\n",$x,$x2,$schrep[$_[0]],$schadj[$_[0]],$schfnt[$_[0]],$schrank[$_[0]],$schcate[$_[0]],$schopt[$_[0]],$schitem[$_[0]] ) ; 
}


#  "20050101"  形式を  "2005/01/01" 形式に変換する
sub num_to_date {
return(substr($_[0],0,4) . "/" . substr($_[0],4,2) . "/" . substr($_[0],6,2)); 
}



                # item の削除
sub delete_data {
local($i,$del,$ddate ) ;

$del = $webdata{'key'} ; 
$ddate = $schdate[$del] ; 

$cur = $webdata{'cur'} ;    
$cur_yy = int($cur / 100) ; 
$cur_mm = $cur % 100 ; 


open (OUT,"> schdata.txt");
for ( $i = 0 ; $i <= $nsch ; $i++ ) {
    if ( $i != $del ) {
        &write_schdata_line($i)
    }
}
close(OUT); 

&read_schdata ;

}


############################################################
# 月末の数字を求める
# 引き数：年、月
# 戻り値：月末の数字
#
sub getgetumatu {	
	local($year,$mon) = @_;
	if($mon != 2){
		return(@monthday[$mon-1]);
	}else{
		if(&leapyear($year)){ return(29); }
		else{ return(28); }
	}
}

############################################################
# 閏年の判定
# 引き数：年
# 戻り値：1=閏年、0=閏年じゃない
#
sub leapyear {
	local($year) = @_;

	if(($year % 4 == 0 && $year % 100 != 0) || $year % 400 == 0){
		return 1;
	}else{
		return 0;
	}
}


############################################################
# 曜日を求める
# 引き数：年(4桁 2000以上)、月、日
# 戻り値：曜日の数字
# 0="日",1="月",2="火",3="水",4="木",5="金",6="土"
#
sub day_week {
local($year,$mon,$day) = @_;
local($daynum,$i);

$daynum = 0;
$mon = $mon - 1;
$daynum = ($year-2000)*365 + int(($year-1997)/4) ; 

for($i = 0; $i < $mon; $i++){
	$daynum += $monthday[$i];
	if($i == 1 && &leapyear($year)){ $daynum++; }
}
$daynum += $day;     # 2000年1月1日 を 1とする日数

return(($daynum+5) % 7 )     # 2000年1月1日 は土曜日なので
}

sub get_holiday {
local($i,$j,$y,$m,$d,@x) ;

open (IN,"holiday.txt");
for ( $j = 0 ; $j <= 6 ; $j++ ) { $hdweek[$j] = 0 ; } 
$hdweek[0] = 1 ;   # 既定値は土日
$hdweek[6] = 1 ; 

$i = 0 ; 
$hdfestival_include = 1 ;   # 未サポート

while ($xx = <IN>) { 
    @x = split(";",$xx ) ;
    if ( index($x[0],"w=") != -1 ) {
        print "OK" ;
        for ( $j = 0 ; $j <= 6 ; $j++ ) { $hdweek[$j] = 0 ; } 
        for ( $j = 2 ; $j <= length($x[0]) ; $j++ ) {
            $hdweek[substr($x[0],$j,1)] = 1 ; 
        }
        next ;
    }
    if ( index($x[0],"f=") != -1 ) {
        if ( substr($x[0],2,1) eq "n" ) { $hdfestival_include = 0 ;  }
        next ;
    }
    @hdate = split("/",$x[0]) ; 

    if (@hdate[0] == "*" ) { $y = 0 ; }
    else { $y = @hdate[0] ;  }
    $m = @hdate[1] ; 
    $d = @hdate[2] ; 
    
    $hdmmdd[$i] = $y * 10000 + $m  * 100 + $d ; 
    $hdtype[$i] = $x[1] ;
    $hdcmt[$i] = $x[2] ;     # 休日の内容(今は未使用)
    $i++;

}
close(IN);

}

#  休日チェック
#     引数  0 .. 年  1 .. 月  2 .. 日
#     返却値1  0  平日  1  公休日  2 土曜日 3 私休日
sub check_holiday {
local($i , $ckdate, $ckdate2, $ho , $wd,$match)  ;
    $ckdate = ($_[0]-2000) * 10000 + $_[1] * 100 + $_[2]  ; 
    $ckdate2 = $_[1] * 100 + $_[2]  ; 

    $wd = &day_week($_[0],$_[1],$_[2]) ; 
    if ( $wd == 0 ) { return(1) ; }    # 日曜日

    $i = 0 ;
    $match = 0 ; 
    foreach $ho (@hdmmdd) {
        if ($ho < 10000 ) {   #  年が省略されている
            if ($ho == $ckdate2 ) {   #  月日だけ比較
                $match = 1 ; 
                last ; 
            }
        }
        else {
            if ($ho == $ckdate ) { 
                $match = 1 ;
                last ;
            }
        }
        $i++;
    }
    if ( $match == 1 && $hdtype[$i] == 0 ) { return(1) ; } 
    if ( $wd == 6 ) { return(2) ; }    # 土曜日

    if ( $match == 1 && $hdtype[$i] == 1 ) { return(3) ; } 
    if ( $hdweek[$wd] == 1 ) { return(3) ;}

    return(0) ; 
}

sub make_link {
local($i )
    &prev_next_month(0) ;
    printf("<a href=\"%s\"><b>前月</b></a>\n",$link_url) ; 
    printf("<a href=\"./sch.cgi?ctype=%d\"><b>今月</b></a>\n",$ctype) ; 
    &prev_next_month(1) ;
    printf("<a href=\"%s\"><b>次月</b></a>\n",$link_url) ; 
    for ( $i = 1 ; $i <=12 ; $i++ ) {
        printf("<a href=\"./sch.cgi?yy=%d&mm=%d&ctype=%d\">%d</a> ",$cur_yy,$i,$ctype,$i) ;
    }
    printf("<a href=\"./sch.cgi?yy=%d&mm=%d&ctype=%d\"><b>前年</b></a> \n",$cur_yy-1,$cur_mm,$ctype) ; 
    printf("<a href=\"./sch.cgi?yy=%d&mm=%d&ctype=%d\"><b>来年</b></a> \n",$cur_yy+1,$cur_mm,$ctype) ; 
    
    printf("<br>\n") ; 
}

sub prev_next_month {
local($yy, $mm)  ;

    if ( $_[0] == 1 ) {    # 次月
        ($yy, $mm) = &next_yymm($cur_yy,$cur_mm) ; 
    }
    else {                # 前月
        ($yy, $mm) = &prev_yymm($cur_yy,$cur_mm) ; 
    }
    $link_url="./sch.cgi?yy=" . $yy . "&mm=" . $mm . "&ctype=" . $ctype ; 
    
}

sub youbi_header {
    local(@yostr,$x,$i,$j) ;

    @yostr = ("日","月","火","水","木","金","土")  ;

    for ( $i = 0 ; $i < 7 ; $i++ )  {
        $j = $i + $start_wk ; 
        if ( $j >= 7 ) { $j = $j - 7 ; } 
        $x = $yostr[$j]  ; 

        if ( $cal_mini_flg == 1 ) {
            printf("<td align=center width=%d><font color=%s>%s</font></td>",$width,$youbi_ttl_color[$j],$x) ; 
        }
        else {
            printf("<td align=center bgcolor=%s width=%d><font color=%s>%s</font></td>",$youbi_ttl_bgcolor[$j],$width,$youbi_ttl_color[$j],$x) ; 
        }
    }

}

sub header {
print <<EOF;
Content-type: text/html;

<html><head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<title>sch</title>
<script language=javascript type="text/javascript">
<!--
function overCal(ev) {
	if(!ev||!ev.srcElement) reutrn;var e=ev.srcElement;
	while(e&&e.tagName!="TD") {e=e.parentElement;}
	if(e&&e.className=="sc") {e.style.background="$cursor_bg";e.style.cursor="hand";}
}
function outCal(ev) {
	if(!ev||!ev.srcElement) return;var e=ev.srcElement;
	while(e&&e.tagName!="TD") {e=e.parentElement;}
	if(e&&e.className=="sc") {e.style.background=e.bgColor;e.style.backgroundImage='url(' + e.background + ')';}
}
function add(id,ctype) {
	location.href="./sch.cgi?mode=1&key="+id+"&ctype="+ctype;
}
//-->
</script>
<style type="text/css">
<!-- 
  A { text-decoration: none; }
  table.list { 
    margin-left:20;
    margin-right:20 ;
  }
  table.minical {
    margin-left:20;
    margin-right:20 ;
  }
  .main_style  {font-size: $main_char_size pt; }
  .mini_style  {font-size: $mini_char_size pt; }
  .year_style  {font-size: $year_char_size pt; }
  .list_style  {font-size: $list_char_size pt; }
  .daynumber   {font-size: $daynumber_size pt; font-weight : bold; }
  

-->

</style>

</head>
<body link="#000000" vlink="#000000" alink="#000000" bgcolor="$bgcolor" background="$bgimage">
EOF
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
<form method="POST" action="sch.cgi">
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
<input type="submit" name="cfg_ng" value="キャンセル"> 
<input type="hidden" name="ctype" value="$ctype"> 
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

#  スケジュール追加、編集画面 htmlヘッダ
sub add_edit_header {
print << "EOF";
Content-type: text/html;

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<meta http-equiv="Content-Style-Type" content="text/css">
<title>sch追加</title>
<SCRIPT TYPE="text/javascript"> 
<!-- 

function set(){ 

document.form1.item.value = document.form1.teikei.options[document.form1.teikei.selectedIndex].value ; 
} 
// --> 
</SCRIPT> 
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

input.a { background-color: #85B9E9; } 
.red { color: red; } 

.btn { 
width : 80px ; background-color : #a3db91 ; border: medium #633aed double; 
} 
.itemcl { 
border: 1px #1e9126 solid; background-color : #cefdec ; 
} 

-->
</style></head><body><center><table><tbody><tr>
<td width="100"></td>
<td class="ttl">*** スケジュール追加 ***</td>
<td width="100"></td>
</tr></tbody></table></center><br><br>
<center>
<table border="0" cellspacing="0" cellpadding="2">
<tbody><tr>
<td bgcolor="#c700ff">
<table cellspacing="2" border="0" cellpadding="15" bgcolor="#efe5fc">
<tbody><tr><td>
EOF
}

#   スケジュール追加画面
sub display_add {
local($i,$s,$yy,$mm,$dd,$x) ; 
$yy = yy_mask($_[0]) ; 
$mm = mm_mask($_[0]) ; 
$dd = dd_mask($_[0]) ; 

$cur_yy = $yy ;
$cur_mm = $mm ;

&add_edit_header ; 

print << "EOF";
<form method="POST" action="sch.cgi" name="form1">
<select name="yy1">
EOF

for ( $i = $start_year ; $i <= $end_year ; $i++ ) {
    $s = "" ; 
    if ( $i == $yy ) { $s = "selected" ; }
    printf("    <option value=\"%d\" %s>%d年</option>\n",$i,$s,$i) ; 
}

print << "EOF";
</select>
<select name="mm1" >
EOF

for ( $i = 1 ; $i <= 12 ; $i++ ) {
    $s = "" ; 
    if ( $i == $mm ) { $s = "selected" ; }
    printf("    <option value=\"%d\" %s>%d月</option>\n",$i,$s,$i) ; 
}

print << "EOF";
</select>
<select name="dd1">
EOF

for ( $i = 1 ; $i <= 31 ; $i++ ) {
    $s = "" ; 
    if ( $i == $dd ) { $s = "selected" ; }
    printf("    <option value=\"%d\" %s>%d日</option>\n",$i,$s,$i) ; 
}

print << "EOF";
</select> ～

<select name="yy2">
    <option value="0" selected>--</option>
    <option value="2012">2012年</option>
    <option value="2013">2013年</option>
    <option value="2014">2014年</option>
    <option value="2015">2015年</option>
    <option value="2016">2016年</option>
    <option value="2017">2017年</option>
    <option value="2018">2018年</option>
    <option value="2019">2019年</option>
    <option value="2020">2020年</option>
</select>
<select name="mm2">
    <option value="0" selected>--</option>
EOF

for ( $i = 1 ; $i <= 12 ; $i++ ) {
    printf("    <option value=\"%d\">%d月</option>\n",$i,$i) ; 
}

print << "EOF";
</select>
<select name="dd2">
    <option value="0" selected>--</option>
EOF

for ( $i = 1 ; $i <= 31 ; $i++ ) {
    printf("    <option value=\"%d\">%d日</option>\n",$i,$i) ; 
}

print << "EOF";
</select> <br>

<br>
項目 <input size="50" type="text" name="item" class=itemcl>&nbsp;&nbsp;
定型 <select name="teikei">
EOF

foreach $x (@fixed_item) {
    printf("<option value=\"%s\">%s</option>\n",$x,$x) ;
}

print << "EOF";
</select>
<input type="button" value="コピー" onClick="set()">
<br><br>
文字色 
<select name="chcl">
    <option value="0" selected>--</option>
    <option value="1" >赤</option>
    <option value="2" >緑</option>
    <option value="3" >青</option>
    <option value="4" >黄</option>
    <option value="5" >紫</option>
    <option value="6" >シアン</option>
    <option value="7" >水</option>
    <option value="8" >橙</option>
    <option value="9" >白</option>
    <option value="10" >黒</option>
</select>
&nbsp; &nbsp; 背景色 
<select name="chbc">
    <option value="0" selected>--</option>
    <option value="1" >赤</option>
    <option value="2" >緑</option>
    <option value="3" >青</option>
    <option value="4" >黄</option>
    <option value="5" >紫</option>
    <option value="6" >シアン</option>
    <option value="7" >水</option>
    <option value="8" >橙</option>
    <option value="9" >白</option>
    <option value="10" >黒</option>
</select>
<br><br>
ランク 
<select name="rank">
    <option value="0" selected>0</option>
    <option value="1" >1</option>
    <option value="2" >2</option>
</select>
&nbsp; &nbsp; カテゴリ 
<select name="cate">
    <option value="0" selected>--</option>
EOF

for ( $i = 1 ; $i <= $ncate ; $i++ ) {
    printf("    <option value=\"%d\">%s</option>\n",$i,$category[$i]) ; 
}

print << "EOF";
</select>
<br><br>
繰り返し<br>
&nbsp; &nbsp; <input type="radio" name="rep" value="rep0" checked> なし<br>
&nbsp; &nbsp; <input type="radio" name="rep" value="rep1"> 毎週 &nbsp; 
<input type="checkbox" name="repweek" value="0"> 日 
<input type="checkbox" name="repweek" value="1"> 月 
<input type="checkbox" name="repweek" value="2"> 火 
<input type="checkbox" name="repweek" value="3"> 水 
<input type="checkbox" name="repweek" value="4"> 木 
<input type="checkbox" name="repweek" value="5"> 金 
<input type="checkbox" name="repweek" value="6"> 土 <br>
&nbsp; &nbsp; <input type="radio" name="rep" value="rep2"> 毎月 &nbsp; 
<select name="repdd">
    <option value="0" selected>--</option>
EOF

for ( $i = 1 ; $i <= 31 ; $i++ ) {
    printf("    <option value=\"%d\">%d日</option>\n",$i,$i) ; 
}

print << "EOF";
</select><br>

&nbsp; &nbsp; <input type="radio" name="rep" value="rep3"> 毎月 &nbsp; 
<input type="checkbox" name="repcnt" value="1"> 第1 
<input type="checkbox" name="repcnt" value="2"> 第2 
<input type="checkbox" name="repcnt" value="3"> 第3 
<input type="checkbox" name="repcnt" value="4"> 第4 
<input type="checkbox" name="repcnt" value="5"> 第5 
<input type="checkbox" name="repcnt" value="9"> 最終 
<select name="repww">
    <option value="0" class=red>日曜</option>
    <option value="1">月曜</option>
    <option value="2">火曜</option>
    <option value="3">水曜</option>
    <option value="4">木曜</option>
    <option value="5">金曜</option>
    <option value="6" class=red>土曜</option>
</select>  &nbsp;<br>

&nbsp; &nbsp; <input type="radio" name="rep" value="rep4"> 毎年 &nbsp; 
<select name="rep4mm">
    <option value="0" selected>--</option>
EOF

for ( $i = 1 ; $i <= 12 ; $i++ ) {
    printf("    <option value=\"%d\">%d月</option>\n",$i,$i) ; 
}

print << "EOF";
</select>
<select name="rep4dd">
    <option value="0" selected>--</option>
EOF

for ( $i = 1 ; $i <= 31 ; $i++ ) {
    printf("    <option value=\"%d\">%d日</option>\n",$i,$i) ; 
}

print << "EOF";
</select> <br><br>
調整&nbsp;&nbsp;&nbsp;条件 
<select name="adjcond">
    <option value="0" selected>--</option>
    <option value="1" >休日を変更</option>
    <option value="2" >日曜日を変更</option>
</select>
&nbsp;&nbsp;動作
<select name="adj">
    <option value="0" selected>--</option>
    <option value="1" >前</option>
    <option value="2" >後</option>
    <option value="3" >無効</option>
</select>
<br><br>
<input type="submit" class="btn" name="add_ok" value="登録"> &nbsp; &nbsp; 
<input type="submit" class="btn" name="add_ng" value="キャンセル"> 
<input type="hidden" name="key" value="$_[0]">
<input type="hidden" name="ctype" value="$ctype"> 
<input type="hidden" name="cur_yy" value="$cur_yy"> 
<input type="hidden" name="cur_mm" value="$cur_mm"> 
</form></td></tr></tbody></table>
</td></tr></tbody></table>
</center></body></html>
EOF

}

#  スケジュール編集画面
sub display_edit {
local($i,$x,$s,$yy,$mm,$dd,$yy2,$mm2,$dd2,$rep,$type,@ck,$xx) ; 
local($cl,$bc,$cur,$rank,$cate,$adjcond,$adj) ; 

@adjcondname = ("--","休日を変更","日曜日を変更") ; 
@adjname = ("--","前","後","無効") ; 

$cur = $webdata{'cur'} ; 

$item = $schitem[$_[0]] ;
$sdate = $schdate[$_[0]] ;
$rep = $schrep[$_[0]] ;
$rank = $schrank[$_[0]] ;
$cate = $schcate[$_[0]] ;
#if ( $cate eq "" ) { $cate = "0" ; } 
$adjcond = substr($schadj[$_[0]],0,1) ;
$adj = substr($schadj[$_[0]],1,1) ;


$type = substr($rep,0,1) ;
$yy = &yy_mask($sdate) ; 
$mm = &mm_mask($sdate) ; 
$dd = &dd_mask($sdate) ; 

$yy2 = &yy_mask($schdate2[$_[0]]) ; 
if ( $yy2 == 9999 ) {
    $yy2 = 0 ; $mm2 = 0 ; $dd2  = 0 ; 
}
else {
$mm2 = &mm_mask($schdate2[$_[0]]) ; 
$dd2 = &dd_mask($schdate2[$_[0]]) ; 
}

($cl,$bc) = &font_analize($_[0]) ;  # 文字色、背景色
$i = 0 ; 
foreach $x (@cname) {
    if ( $cl eq $x ) { $cl = $i ;  break ; } 
    $i++ ; 
}

$i = 0 ; 
foreach $x (@cname) {
    if ( $bc eq $x ) { $bc = $i ;  break ; } 
    $i++ ; 
}


&add_edit_header ; 

print << "EOF";
<form method="POST" action="sch.cgi" name="form1">
<select name="yy1">
EOF

######  開始日付  ########

for ( $i = $start_year ; $i <= $end_year ; $i++ ) {
    $s = "" ; 
    if ( $i == $yy ) { $s = "selected" ; }
    printf("    <option value=\"%d\" %s>%d年</option>\n",$i,$s,$i) ; 
}

printf("</select>\n<select name=\"mm1\">\n") ;

for ( $i = 1 ; $i <= 12 ; $i++ ) {
    $s = "" ; 
    if ( $i == $mm ) { $s = "selected" ; }
    printf("    <option value=\"%d\" %s>%d月</option>\n",$i,$s,$i) ; 
}

printf("</select>\n<select name=\"dd1\">\n") ; 

for ( $i = 1 ; $i <= 31 ; $i++ ) {
    $s = "" ; 
    if ( $i == $dd ) { $s = "selected" ; }
    printf("    <option value=\"%d\" %s>%d日</option>\n",$i,$s,$i) ; 
}


######  終了日付  ########

printf("</select> ～\n\n<select name=\"yy2\">\n") ;

if ($yy2 == 0 ) {
    printf("<option value=\"0\" selected>--</option>\n") ;
}
else {
    printf("<option value=\"0\">--</option>\n") ; 
}
for ( $i = $start_year ; $i <= $end_year ; $i++ ) {
    $s = "" ; 
    if ( $i == $yy2 ) { $s = "selected" ; }
    printf("    <option value=\"%d\" %s>%d年</option>\n",$i,$s,$i) ; 
}

printf("</select>\n<select name=\"mm2\">\n" );

if ($yy2 == 0 ) {
    printf("<option value=\"0\" selected>--</option>\n") ;
}
else {
    printf("<option value=\"0\">--</option>\n") ; 
}
for ( $i = 1 ; $i <= 12 ; $i++ ) {
    $s = "" ; 
    if ( $i == $mm2 ) { $s = "selected" ; }
    printf("    <option value=\"%d\" %s>%d月</option>\n",$i,$s,$i) ; 
}

printf("</select>\n<select name=\"dd2\">\n" ) ; 

if ($yy2 == 0 ) {
    printf("<option value=\"0\" selected>--</option>\n") ;
}
else {
    printf("<option value=\"0\">--</option>\n") ; 
}
for ( $i = 1 ; $i <= 31 ; $i++ ) {
    $s = "" ; 
    if ( $i == $dd2 ) { $s = "selected" ; }
    printf("    <option value=\"%d\" %s>%d日</option>\n",$i,$s,$i) ; 
}

print << "EOF";
</select> <br>

<br>
項目 <input size="50" type="text" name="item" class=itemcl value="$item"> &nbsp;&nbsp;
定型 <select name="teikei">
EOF

foreach $x (@fixed_item) {
    printf("<option value=\"%s\">%s</option>\n",$x,$x) ;
}

print << "EOF";
</select>
<input type="button" value="コピー" onClick="set()">
<br><br>
文字色 
<select name="chcl">
EOF

for ($i = 0 ; $i <= 10 ; $i++ ) {
    $s = "" ; 
    if ( $cl == $i ) { $s = "selected" ; } 
    printf("    <option value=\"%d\" %s>%s</option>\n",$i,$s,$cname2[$i]) ; 
}

print << "EOF";
</select>
&nbsp; &nbsp; 背景色 
<select name="chbc">
EOF

for ($i = 0 ; $i <= 10 ; $i++ ) {
    $s = "" ; 
    if ( $bc == $i ) { $s = "selected" ; } 
    printf("    <option value=\"%d\" %s>%s</option>\n",$i,$s,$cname2[$i]) ; 
}

print << "EOF";
</select>
<br><br>
ランク 
<select name="rank">
EOF

for ($i = 0 ; $i <= 2 ; $i++ ) {
    $s = "" ; 
    if ( $rank == $i ) { $s = "selected" ; } 
    printf("    <option value=\"%d\" %s>%d</option>\n",$i,$s,$i) ; 
}

print << "EOF";
</select>
&nbsp; &nbsp; カテゴリ 
<select name="cate">
EOF

for ($i = 0 ; $i <= $ncate ; $i++ ) {
    $s = "" ; 
    if ( $cate == $i ) { $s = "selected" ; } 
    printf("    <option value=\"%d\" %s>%s</option>\n",$i,$s,$category[$i]) ; 
}

print << "EOF";
</select>
<br><br>
繰り返し<br>
EOF

if ( $type == 0 ) { 
printf("&nbsp; &nbsp; <input type=\"radio\" name=\"rep\" value=\"rep0\" checked> なし<br>\n" ) ;
}
else {
printf("&nbsp; &nbsp; <input type=\"radio\" name=\"rep\" value=\"rep0\"> なし<br>\n" ) ;
}


###### 毎週特定曜日  ########
for ( $i = 0 ; $i < 7 ; $i++ ) {
    @ck[$i] = 0 ; 
}

$s = "" ; 
if ( $type == 3 ) { 
    $s = "checked" ; 
    for( $j = 1 ; $j <= length($rep)-1 ; $j++ ) {
           @ck[substr($rep,$j,1)] = 1  ; 
    }
}
printf("&nbsp; &nbsp; <input type=\"radio\" name=\"rep\" value=\"rep1\" %s> 毎週 &nbsp; \n",$s ) ;

for ( $i = 0 ; $i < 7 ; $i++ ) {
    $s = "" ; 
    if ( @ck[$i] == 1 ) {  $s = "checked" ; } 
    printf("<input type=\"checkbox\" name=\"repweek\" value=\"%d\" %s> %s\n",$i,$s,@wkname[$i]) ; 
}
printf("<br>\n") ; 


###### 毎月特定日 ########

$s = "" ; 
$xx =  0 ; 
if ( $type == 1 ) { 
    $s = "checked" ; 
    $xx = substr($rep,1,2) ;
}

printf("&nbsp; &nbsp; <input type=\"radio\" name=\"rep\" value=\"rep2\" %s> 毎月 &nbsp;\n",$s) ; 
printf("<select name=\"repdd\">\n") ; 

if ( $xx == 0 ) {
    printf("    <option value=\"0\" selected>--</option>\n") ;
}
else {
    printf("    <option value=\"0\">--</option>\n") ;
}
for ( $i = 1 ; $i <= 31 ; $i++ ) {
    $s = "" ; 
    if ( $xx == $i ) { $s = "selected" ; }
    printf("    <option value=\"%d\" %s>%d日</option>\n",$i,$s,$i) ; 
}
printf("</select><br>\n") ;


###### 第n曜 ########

for ( $i = 0 ; $i <= 9 ; $i++ ) {
    @ck[$i] = 0 ; 
}
$s = "" ;
$wk = 9 ; 
if ( $type == 4 ) { 
    $s = "checked" ; 
    $wk = substr($rep,1,1) ;
    for( $j = 2 ; $j <= length($rep)-1 ; $j++ ) {
           @ck[substr($rep,$j,1)] = 1  ; 
    }
}

printf("&nbsp; &nbsp; <input type=\"radio\" name=\"rep\" value=\"rep3\" %s> 毎月 &nbsp; \n",$s)  ; 

for ( $i = 1 ; $i <= 5 ; $i++ ) {
    $s = "" ;
    if ( @ck[$i] == 1 ) { $s = "checked" ; }
    printf("<input type=\"checkbox\" name=\"repcnt\" value=\"%d\" %s> 第%d\n",$i,$s,$i) ; 
}
$s = "" ;
if ( @ck[9] == 1 )  { $s = "checked" ; }
printf("<input type=\"checkbox\" name=\"repcnt\" value=\"9\" %s> 最終\n",$s) ; 
printf("<select name=\"repww\">\n") ; 
for ( $i = 0 ; $i < 7 ; $i++ ) {
    $s = "" ; 
    if ( $wk == $i ) { $s = "selected" ; }
    printf("    <option value=\"%d\" %s>%s</option>\n",$i,$s,$wkname[$i]);
}
printf("</select>  &nbsp;<br>\n" ) ;

###### 毎年特定日 ########


$s = "" ;
$mm2 = 0 ;
$dd2 = 0 ;

if ( $type == 2 ) { 
    $s = "checked" ; 
    $mm2 = substr($rep,1,2) ;
    $dd2 = substr($rep,3,2) ;
}

printf("&nbsp; &nbsp; <input type=\"radio\" name=\"rep\" value=\"rep4\" %s> 毎年 &nbsp; \n",$s) ;
printf("<select name=\"rep4mm\">\n") ;
if ( $mm2 == 0 ) {
    printf("    <option value=\"0\" selected>--</option>\n" ) ;
}
else {
    printf("    <option value=\"0\" >--</option>\n" ) ;
}

for ( $i = 1 ; $i <= 12 ; $i++ ) {
    $s = "" ; 
    if ( $mm2 == $i ) {$s = "selected" ;  } 
    printf("    <option value=\"%d\" %s>%d月</option>\n",$i,$s,$i) ; 
}

printf("</select>\n") ;
printf("<select name=\"rep4dd\">\n");

if ( $dd2 == 0 ) {
    printf("    <option value=\"0\" selected>--</option>\n") ; 
}
else {
    printf("    <option value=\"0\" >--</option>\n" ) ;
}

for ( $i = 1 ; $i <= 31 ; $i++ ) {
    $s = "" ; 
    if ( $dd2 == $i ) {$s = "selected" ;  } 
    printf("    <option value=\"%d\" %s>%d日</option>\n",$i,$s,$i) ; 
}

print << "EOF";
</select>
<br><br>
調整&nbsp;&nbsp;&nbsp;条件 
<select name="adjcond">
EOF

for ( $i = 0 ; $i <= 2 ; $i++ ) {
    $s = "" ; 
    if ( $adjcond == $i ) {$s = "selected" ;  } 
    printf("    <option value=\"%d\" %s>%s</option>\n",$i,$s,$adjcondname[$i]) ; 
}

print << "EOF";
</select>
&nbsp;&nbsp;動作
<select name="adj">
EOF

for ( $i = 0 ; $i <= 3 ; $i++ ) {
    $s = "" ; 
    if ( $adj == $i ) {$s = "selected" ;  } 
    printf("    <option value=\"%d\" %s>%s</option>\n",$i,$s,$adjname[$i]) ; 
}

print << "EOF";
</select>
<br><br>
<input type="submit" class="btn" name="edit_ok" value="登録"> &nbsp; &nbsp; 
<input type="submit" class="btn" name="edit_ng" value="キャンセル"> &nbsp; &nbsp; 
<input type="submit" class="btn" name="edit_del" value="削除">
<input type="hidden" name="key" value="$_[0]">
<input type="hidden" name="ctype" value="$ctype"> 
<input type="hidden" name="cur" value="$cur"> 
</form>
</td></tr></tbody></table>
</td></tr></tbody></table>
</center></body></html>
EOF
}

#  日の背景色設定
sub  day_bgcolor 
{
printf("Content-type: text/html\n\n" ) ; 
printf("<html><body>\n") ; 
printf("<b>日の背景色設定</b><br>\n");
printf("<form method=\"POST\" action=\"./sch.cgi\">\n") ; 

printf("年月日(yyyymmdd) <input size=15 type=text name=\"bgdate\" >\n");
printf("色(#xxxxxx) <input size=20 type=text name=\"color\" >\n") ; 
printf("<input type=\"submit\" name=\"day_bgcolor_add\" value=\"追加\"><br>\n") ; 
printf("</form><a href=./sch.cgi>戻る<a/></body></html>\n") ;

}

sub add_day_bgcolor 
{
local($i,$bgdate,$color) ;
$bgdate = $webdata{'bgdate'} ;    
$color = $webdata{'color'} ;    
$i = &search_daybgcolor($bgdate) ; 
if ( $i == -1 ) {
    $nsch++ ; 
    $schdate[$nsch]  = $bgdate ;
    $schdate2[$nsch]  = 99991231 ;
    $schitem[$nsch]  = $color ;
    $schopt[$nsch] = 1 ;
}
else {
    $schdate[$i]  = $bgdate ;
    $schdate2[$i]  = 99991231 ;
    $schitem[$i]  = $color ;
    $schopt[$i] = 1 ;
}

&write_schdata ;
}

#     日の背景色が設定されているか
sub search_daybgcolor {
local($i,$key ) ;

$key = $_[0]; 
for ( $i = 0 ; $i <= $nsch ; $i++ ) {
    if ($schopt[$i] == 1 and $schdate[$i] == $key ) {
        return($i) ;
    }
}
return(-1) ;

}

#     指定した日の背景色を返す
sub check_daybgcolor {
local($i,$key ) ;

$key = $_[0] * 10000 + $_[1] * 100 + $_[2]; 


for ( $i = 0 ; $i <= $nsch ; $i++ ) {

    if ($schopt[$i] == 1 && $schdate[$i] == $key ) {
        return($schitem[$i]) ;
    }
}
return("") ;
}

