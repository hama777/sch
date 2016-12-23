#!/usr/local/bin/perl

# 定型項目編集

require "cgi-lib.pl";

local($i,$j,$k,$ho,$tt,$del,$addok) ; 


&ReadParse(\%webdata);

$del = $webdata{'del'} ; 
$add = $webdata{'add'} ; 



if ( $del eq "削除" ) {
    &del_item;
    &display  ;
    exit ;
}

if ( $add eq "追加" ) {
    &add_item;
    &display  ;
    exit ;
}


&display ; 
exit ;

# データ一覧
sub display {
local($xx) ; 

printf("Content-type: text/html\n\n" ) ; 
printf("<html><body>\n") ; 
printf("<b>定型項目編集</b><br>\n");
printf("<form method=\"POST\" action=\"./sch_item.cgi\">\n") ; 
printf("<table>") ; 



open (IN,"item.txt");
$i = 0 ; 


while ($xx = <IN>) { 
    printf("<tr><td><input type=\"checkbox\" name=\"del%d\" value=\"1\"></td><td>",$i+1) ; 

#    printf("<a href=./sch_item?edit=%d>編集</a> ",$i+1) ; 
    printf("%s</td></tr>",$xx ) ; 
    $i++; 
}
close(IN); 
printf("</table><br><input type=\"submit\" name=\"del\" value=\"削除\"><br><br><input size=20 type=text name=\"additem\" style=\"background-color : #ffffbb;\">
<input type=\"submit\" name=\"add\" value=\"追加\"><br>\n") ; 
printf("</form><a href=./sch_setup.cgi>戻る<a/></body></html>\n") ;


}


sub del_item {
local($xx,$i,$cnt,$val) ; 

    open(DBG, "> debug.txt");
    print(DBG  "del_todo\n"  );

    open (IN,"item.txt");
    $i = 0 ; 
    while ($xx = <IN>) { 
        $i++;
        $schdata[$i] = $xx ; 
    }
    close(IN);
    $cnt = $i ; 

    open(OUT, "> item.txt");
    for ($i=1 ; $i <= $cnt ; $i++ ){
        $val = $webdata{'del' . $i } ; 
        print(DBG  $i . $val . "\n"  );

        if ( $val ne "1"  ) {
            print(DBG  "del \n"  );
            print(OUT  $schdata[$i] );
        }
    }
    close(OUT);
    close(DBG);


}

sub add_item {
    $additem = $webdata{'additem' } ; 
    open (OUT,">> item.txt");
    printf(OUT "%s\n",$additem) ; 
    close(OUT) ;
}
