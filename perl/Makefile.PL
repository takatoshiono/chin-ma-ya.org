use inc::Module::Install;

name 'Chinmaya';
all_from 'lib/Chinmaya.pm';

build_requires 'Test::More';

requires 'Web::Scraper';
requires 'Geo::Coder::Google';
requires 'Class::Accessor';
requires 'URI';
requires 'DBI';
requires 'DBD::SQLite';
requires 'Net::Twitter';

auto_include;
WriteAll;

