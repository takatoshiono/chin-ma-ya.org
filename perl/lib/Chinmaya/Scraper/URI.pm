package Chinmaya::Scraper::URI;

use strict;
use warnings;
use base qw/ Class::Accessor::Fast/;

use URI;

__PACKAGE__->mk_accessors(
    qw/ ht k kh tk chu ko s /
);

sub new {
    my $class = shift;
    my $self = $class->SUPER::new(@_);
    $self->init();
    $self;
}

sub init {
    my $self = shift;

    $self->ht( URI->new('http://www.chin-ma-ya.net/tenpo/ht.html') );  # 北海道・東北
    $self->k( URI->new('http://www.chin-ma-ya.net/tenpo/k.html') );   # 関東
    $self->kh( URI->new('http://www.chin-ma-ya.net/tenpo/kh.html') );  # 甲信越・北陸
    $self->tk( URI->new('http://www.chin-ma-ya.net/tenpo/tk.html') );  # 東海・近畿
    $self->chu( URI->new('http://www.chin-ma-ya.net/tenpo/chu.html') ); # 中国
    $self->ko( URI->new('http://www.chin-ma-ya.net/tenpo/ko.html') );  # 九州・沖縄
    $self->s( URI->new('http://www.chin-ma-ya.net/tenpo/s.html') ); # 四国
}

1;

