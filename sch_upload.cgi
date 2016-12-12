#!/usr/local/bin/perl
#  2007.03.08  Ver.  1.34 対応

# データアップロード

require "cgi-lib.pl";

local($i,$j,$k,$ho,$tt) ; 


&ReadParse(\%webdata);


&list_data ; 
exit ;

# データ一覧
sub list_data {
local($xx) ; 

printf("Content-type: text/html\n\n" ) ; 

open (OUT,"> schdatanew.txt");

$xx = $webdata{'filen'} ; 
printf(OUT "%s",$xx) ; 

close(OUT); 

$ret = rename("schdata.txt" , "schdatasv.txt" );

if ( $ret == 0 ) {
    printf("schdata.txt rename error \n") ; 
    return  ;
}

$ret = rename("schdatanew.txt" , "schdata.txt" );

if ( $ret == 0 ) {
    printf("schdatanew.txt rename error \n") ; 
    return  ;
}


printf("OK\n");


}


