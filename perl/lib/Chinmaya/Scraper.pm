package Chinmaya::Scraper;

use strict;
use warnings;
use base qw/ Class::Accessor::Fast /;

use Web::Scraper;
use Geocoder;
use Chinmaya::Scraper::URI;
use Carp;

__PACKAGE__->mk_accessors(
    qw/ uri geocoder /
);

our $VERSION = '0.01';

sub new {
    my $class = shift;
    my $self = $class->SUPER::new({
        uri      => Chinmaya::Scraper::URI->new(),
        geocoder => Geocoder->new(),
    });
    $self;
}

# 指定されたエリアの店舗情報をスクレイプして位置情報を取得して返す
sub get_shops {
    my ($self, $area) = @_;

    my $uri = $self->uri->$area()
        or croak "Cannot find URI like $area";

    my ($shop_names, $infos) = $self->_scrape($uri);

    croak "invalid shop info." unless @$shop_names == @$infos;

    my $n_shops = scalar(@$shop_names);
    my @shops;
    for (my $i = 0; $i < $n_shops; $i++) {
        my $info = $self->_extract_info($infos->[$i]);
        $info->{name} = $shop_names->[$i];
        push @shops, $info;
    }

    return \@shops;
}

sub _scrape {
    my ($self, $uri) = @_;

    my $scraper = scraper {
        process 'td.id-14 > b:first-child',
            'shops[]' => 'TEXT';
        process 'td.id-13',
            'infos[]' => 'TEXT';
        result qw/shops infos/
    };
    my $result = $scraper->scrape($uri);

    return wantarray ? @$result{qw/shops infos/} : $result;
}

sub _extract_info {
    my ($self, $info) = @_;

    my @fields  = split / /, $info;
    my $address = $self->_trim(shift @fields);
    my $extra   = $self->_trim(join q{}, @fields);

    my ($lat, $lng);
    my $addr = $address;
    while (1) {
        ($lat, $lng) = $self->geocoder->get_lat_lng($addr);
        last if ($lat and $lng);
        # 取得できなかったら末尾を１文字削ってみる
        $addr = substr($addr, 0, -1);
        last unless $addr;
    }

    return {
        address => $address,
        extra => $extra,
        latitude => $lat,
        longitude => $lng,
    };
}

sub _trim {
    my ($self, $str) = @_;
    $str =~ s/\s+//g;
    $str;
}

1;

__END__

=head1 NAME

Chinmaya::Scraper - Scrape chin-ma-ya shops.

=head1 SYNOPSIS

    my $scraper = Chinmaya::Scraper->new();
    my $shops = $scraper->get_shops('k'); # get shops in 関東

=head1 DESCRIPTION

Available areas are

=item ht

北海道・東北

=item k

関東

=item kh

甲信越・北陸

=item tk

東海・近畿

=item chu

中国

=item ko

九州・沖縄

=cut
