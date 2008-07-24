package Geocoder;
use strict;
use warnings;
use Geo::Coder::Google;
use base qw/Class::Accessor::Fast/;

__PACKAGE__->mk_accessors(qw/
	apikey geocorder
/);

sub new {
	my $class = shift;
	my $self = $class->SUPER::new(@_);
	$self->init();
	$self;
}

sub init {
	my $self = shift;
	$self->apikey('ABQIAAAAS2GR3nbO3xhKL2p1o_b5fBRPHsmlLL6wcQezZRl8E8AtCCqk4RSKdN0PdalrWPuHCQa-kH-nLv0s9Q');
	$self->geocorder(Geo::Coder::Google->new(apikey => $self->apikey));
}

sub get_lat_lng {
	my ($self, $address) = @_;
    my $location = $self->geocorder->geocode(location => $address);
    my $coordinates = $location->{Point}{coordinates};
    return @$coordinates[qw/1 0/];
}

1;

