#!/usr/local/bin/perl
#  2006.11.27  Ver.  1.34 対応

# データ表示  一括削除

require "cgi-lib.pl";

local($i,$j,$k,$ho,$tt) ; 


&ReadParse(\%webdata);

$del = $webdata{'del'} ; 

if ( $del eq "削除" ) {
    &del_item;
    &list_data  ;
    exit ;
}



&list_data ; 
exit ;

# データ一覧
sub list_data {
local($xx) ; 

printf("Content-type: text/html\n\n" ) ; 
printf("<html><body>\n") ; 
printf("<b>データ一覧</b><br>\n");
printf("<form method=\"POST\" action=\"./sch_list.cgi\">\n") ; 
printf("<table border=0 bgcolor=#4f23f7 cellspacing=0 cellpadding=0><tr><td>\n<table cellspacing=1 border=0 cellpadding=0>") ; 
printf("<tr bgcolor=#bca3ff><td>削除</td><td>日付</td><td>属性</td><td>データ</td></tr>\n");

open (IN,"schdata.txt");
$i = 0 ; 


while ($xx = <IN>) { 
    $bg = "#ffffff" ; 
    if ( $i % 2 == 1 ) { $bg = "#ffffdd" ;  }
    printf("<tr bgcolor=%s><td><input type=\"checkbox\" name=\"del%d\" value=\"1\"></td><td>",$bg,$i+1) ; 

    @key = split("	",$xx ) ;
    @sdata = split(";" , $key[0],2 ) ; 

    printf("&nbsp;%s&nbsp;</td><td>&nbsp;%s&nbsp;</td><td>&nbsp;%s&nbsp;</td></tr>",$sdata[0],$sdata[1],$key[1] ) ; 
    $i++; 
}
close(IN); 
printf("</td></tr></table></table><br><input type=\"submit\" name=\"del\" value=\"削除\"></form><br>\n") ; 
printf("<a href=./sch_setup.cgi>戻る</a></body></html>\n") ;


}


sub del_item {
local($xx,$i,$cnt,$val) ; 

    open(DBG, "> debug.txt");
    print(DBG  "del_todo\n"  );

    open (IN,"schdata.txt");
    $i = 0 ; 
    while ($xx = <IN>) { 
        $i++;
        $schdata[$i] = $xx ; 
    }
    close(IN);
    $cnt = $i ; 

    open(OUT, "> schdata.txt");
    for ($i=1 ; $i <= $cnt ; $i++ ){
        $val = $webdata{'del' . $i } ; 
        print(DBG  $i . $val . "\n"  );

        if ( $val ne "1"  ) {
            print(OUT  $schdata[$i] );
        }
    }
    close(OUT);
    close(DBG);


}

