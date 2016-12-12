#!/usr/local/bin/perl
#  2007.03.08  Ver.  1.34 対応

# データ表示  一括削除

require "cgi-lib.pl";

local($i,$j,$k,$ho,$tt) ; 


&ReadParse(\%webdata);


&list_data ; 
exit ;

# データ一覧
sub list_data {
local($xx) ; 

open (IN,"schdata.txt");
$i = 0 ; 

#printf("Content-type: text/plain\n\n" ) ; 
printf("Content-Type:application/octet-stream\n" ) ; 
printf("Content-Disposition: attachment; filename=\"schdata.txt\"\n\n" ) ; 

while ($xx = <IN>) { 
    printf("%s",$xx) ; 
}
close(IN); 

}


