from crsq.models import ZnInputTag

ZnInputTag.objects.all().delete()
zn = ZnInputTag(heading='reporting_live_list', tag='delhi-india-elections'); zn.save();
zn = ZnInputTag(heading='reporting_live_list', tag='paris-shootings'); zn.save();
zn = ZnInputTag(heading='reporting_live_list', tag='cricket-world-cup-2015'); zn.save();

zn = ZnInputTag(heading='movie_review_list', tag='dolly-ki-doli'); zn.save();
zn = ZnInputTag(heading='movie_review_list', tag='shamitabh'); zn.save();
zn = ZnInputTag(heading='movie_review_list', tag='badlapur'); zn.save();
zn = ZnInputTag(heading='movie_review_list', tag='bombay-velvet'); zn.save();
zn = ZnInputTag(heading='movie_review_list', tag='hawaizaada'); zn.save();
zn = ZnInputTag(heading='movie_review_list', tag='kingsman'); zn.save();
zn = ZnInputTag(heading='movie_review_list', tag='chappie'); zn.save();


