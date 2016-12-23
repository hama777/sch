#!/usr/local/bin/perl

# 休日データ編集

require "cgi-lib.pl";

local($i,$j,$k,$ho,$tt,$del,$addok) ; 


&ReadParse(\%webdata);

$del = $webdata{'del'} ; 
$add = $webdata{'add'} ; 

    open (DBG,"> debug.txt");
    printf(DBG "*** %s\n",$del) ; 
    close(DBG) ;

if ( $del eq "削除" ) {
    &del_item;
    &get_holiday ;
    &display  ;
    exit ;
}

if ( $add eq "追加" ) {
    &add_item;
    &get_holiday ;
    &display  ;
    exit ;
}

&get_holiday ;
&display ; 
exit ;

# データ一覧
sub display {
local($xx,$i,$type) ; 

    printf("Content-type: text/html\n\n" ) ; 
    printf("<html><body>\n") ; 
    printf("<b>休日データ編集</b><br>\n");
    printf("<form method=\"POST\" action=\"./sch_holi.cgi\">\n") ; 
    printf("<table border=0 bgcolor=#91ffbf cellspacing=0 cellpadding=0><tr><td>\n") ; 
    printf("<table cellspacing=1 border=0 cellpadding=0><tr><td>削除</td><td>日付</td><td>私休日</td><td>名前</td></tr>\n") ; 

    $i = 0 ; 
    foreach $ho (@hdmmdd) {
        printf("<tr bgcolor=#ffffff><td><input type=\"checkbox\" name=\"del%d\" value=\"1\"></td><td>",$i+1) ; 

#       printf("<a href=./sch_item?edit=%d>編集</a> ",$i+1) ; 
        if ($ho < 10000 ) {   #  年が省略されている
            printf("&nbsp;*/%02d/%02d&nbsp;</td>",$ho/100,$ho%100) ; 
        }
        else {
            printf("&nbsp;%02d/%02d/%02d&nbsp;</td>",$ho/10000,($ho/100)%100,$ho%100);
        }
        $type = "&nbsp;" ;
        if ($hdtype[$i] == 1 ) {
            $type = "★" ;
        }
        printf("<td align=center>%s</td><td>&nbsp;%s</td></tr>",$type,$hdcmt[$i]) ;
        $i++ ;
    }

printf("</td></tr></table></table><br><input type=\"submit\" name=\"del\" value=\"削除\"><br><br>\n") ; 
printf("年月日(yy/mm/dd) <input size=15 type=text name=\"adddate\" style=\"background-color : #ffffbb;\">\n");
printf("名前 <input size=20 type=text name=\"additem\" style=\"background-color : #ffffbb;\">\n") ; 
printf("私休日 <input type=\"checkbox\" name=\"pri\" value=\"1\">\n") ;
printf("<input type=\"submit\" name=\"add\" value=\"追加\"><br>\n") ; 
printf("</form><a href=./sch_setup.cgi>戻る<a/></body></html>\n") ;


}


sub del_item {
local($xx,$i,$cnt,$val) ; 


    $i = 0 ;
    open (IN,"holiday.txt");
    while ($xx = <IN>) { 
        $i++ ; 
        $hodata[$i] = $xx ; 
    }
    close(IN);
    $cnt = $i ; 

    open(OUT, "> holiday.txt");

    for ($i=1 ; $i <= $cnt ; $i++ ){
        $val = $webdata{'del' . $i } ; 
        if ( $val ne "1"  ) {
            print(OUT  $hodata[$i] );
        }
    }
    close(OUT);
    
}

sub add_item {
    $adddate = $webdata{'adddate' } ; 
    $additem = $webdata{'additem' } ; 
    $pri = $webdata{'pri' } ; 
    if ( $pri eq "" ) { $pri = "0" } ;

    open (OUT,">> holiday.txt");
    printf(OUT "%s;%s;%s\n",$adddate,$pri,$additem) ; 
    close(OUT) ;
}
sub get_holiday {
local($i,$j,$y,$m,$d,@x) ;

open (IN,"holiday.txt");
for ( $j = 0 ; $j <= 6 ; $j++ ) { $hdweek[$j] = 0 ; } 
$hdweek[0] = 1 ;   # 既定値は土日
$hdweek[6] = 1 ; 

$i = 0 ; 
$hdfestival_include = 1 ; 

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
