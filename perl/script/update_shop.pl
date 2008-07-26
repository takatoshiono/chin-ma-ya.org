#!/usr/local/bin/perl

use strict;
use warnings;

use DBI;
use Getopt::Long;
use Net::Twitter;

my %opts;
if (!GetOptions(\%opts,
    'dbfile=s', 'host=s',
    )) {
    exit(1);
}

if ($opts{dbfile} && $opts{host}) {
    my $dbh = DBI->connect("dbi:SQLite:dbname=$opts{dbfile}", '', '')
        or die $DBI::errstr;
    main($dbh);
    $dbh->disconnect();
}
else {
    print "Usage: $0 --dbfile /path/to/db --host chin-ma-ya.org\n";
}

sub main {
    my $dbh = shift;

    my $updater = Updater->new({
        dbh => $dbh,
        host => $opts{host},
    });

    my $candidates = get_update_candidates($dbh);

    foreach my $candidate (@$candidates) {
        my $method = $candidate->{method};
        if ($updater->can($method)) {
            $updater->$method($candidate);
            delete_from_queue($dbh, $candidate->{id});
        }
    }
}

sub get_update_candidates {
    my $dbh = shift;

    my $shops = $dbh->selectall_arrayref(
        'SELECT * FROM queue_shop ORDER BY id',
        { Slice => {} });

    return $shops;
}

sub delete_from_queue {
    my ($dbh, $id) = @_;

    my $sth = $dbh->prepare('DELETE FROM queue_shop WHERE id = ?');
    $sth->execute($id);

    return $sth->rows();
}

1;

package Updater;

use strict;
use warnings;

use LWP::UserAgent;

our $VERSION = '0.01';

sub new {
    my ($class, $args) = @_;

    my $self = bless {
        dbh => $args->{dbh},
        host => $args->{host},
    }, $class;

    return $self;
}

sub ua {
    my $self = shift;

    unless ($self->{ua}) {
        $self->{ua} = LWP::UserAgent->new(
            agent => __PACKAGE__ . "/$VERSION",
        );
    }

    return $self->{ua};
}

sub twitter {
    my $self = shift;

    unless ($self->{twitter}) {
        $self->{twitter} = Net::Twitter->new(
            username => 'tinma',
            password => 'tinmanko!1234',
        );
    }

    return $self->{twitter};
}

sub add {
    my ($self, $src) = @_;

    my $shop = $self->get_shop_by_name($src->{shop_name});
    unless ($shop) {
        # DB
        my $dbh = $self->{dbh};
        my $sth = $dbh->prepare(<<'EOS');
INSERT INTO shops (
    area_id, name, address, latitude, longitude, extra, updated_at, created_at
) VALUES (
    ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now')
)
EOS
        $sth->execute(
            $src->{area_id},
            $src->{shop_name},
            $src->{address},
            $src->{latitude},
            $src->{longitude},
            $src->{extra},
        );
        my $id = $dbh->func('last_insert_rowid');

        # GAE
        my $area = $self->get_area_by_id($src->{area_id});
        my $url = sprintf('http://%s/admin/post/shop', $self->{host});
        $self->ua->post($url, {
            id => $id,
            area => $area->{name},
            name => $src->{shop_name},
            address => $src->{address},
            lat => $src->{latitude},
            lon => $src->{longitude},
            extra => $src->{extra},
        });

        # Twitter
        eval {
            $self->twitter->update(
                sprintf('New Open! 陳麻家 %s http://chin-ma-ya.org/shops/%d',
                    $src->{shop_name}, $id));
        };
        if (my $e = $@) {
            # record error and ignore it.
            print STDERR "failed to add shop($src->{shop_name}) notify on twitter: $e";
        }
    }
}

sub delete {
    my ($self, $src) = @_;

    my $shop = $self->get_shop_by_name($src->{shop_name});
    if ($shop) {
        # GAE
        my $url = sprintf('http://%s/admin/delete/shop', $self->{host});
        $self->ua->post($url, {
            id => $shop->{id},
            name => $shop->{name},
        });

        # DB
        my $dbh = $self->{dbh};
        my $sth = $dbh->prepare(q{UPDATE shops SET deleted_at = datetime('now') WHERE id = ?});
        $sth->execute($shop->{id});

        # Twitter
        eval {
            $self->twitter->update(
                sprintf('Closed.. 陳麻家 %s', $shop->{name}));
        };
        if (my $e = $@) {
            # record error and ignore it.
            print STDERR "failed to delete shop($src->{shop_name}) notify on twitter: $e";
        }
    }
    else {
        print STDERR "cannot find shop($src->{shop_name}) for delete\n";
    }
}

sub get_shop_by_name {
    my ($self, $name) = @_;

    my $dbh = $self->{dbh};
    my $shop = $dbh->selectrow_hashref(
        'SELECT * FROM shops WHERE name = ? AND deleted_at IS NULL',
        undef,
        $name);

    return $shop;
}

sub get_area_by_id {
    my ($self, $id) = @_;

    my $dbh = $self->{dbh};
    my $area = $dbh->selectrow_hashref(
        'SELECT * FROM areas WHERE id = ? AND deleted_at IS NULL',
        undef,
        $id);

    return $area;
}

1;

