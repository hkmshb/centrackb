# Notes


## Hotoro 11KV Feeder (F13E)
This was the first feeder enumerated using the mobile based workflow put together
by the KEDCO ICT team. Captured data were aggregated on the Ona platform (ona.io)
before it was finally moved onto KEDCO's Survey platform (survey.kedco.ng).

### CENTrackb Remarks
When added as a project within CENTrackb, performing a sync operation fails. The
cause? The forms defined for this feeder were named prior to establishing a
standard naming scheme which is adopted by CENTrackb for the sync operation. For
instance one of the forms is named `custform01_mrr' where 01 is the version of
the form and mrr the Business Unit name abbreviated.

The new naming format is of the form `xxxx_yy00_zz` where xxxx is the feeder
code, yy is either cf (capture form) or uf (update form) and zz is the State
name abbreviation.

The code base has been modified to treat XForms for Hotoro 11kV Feeder slightly
different whenever it is encountered.
