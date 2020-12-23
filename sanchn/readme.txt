The file parallel.json contains the checked Udanavarga Sanskrit <--> Tibetan verses using Polyglotta as a base.

Some notes:
1. Polyglotta uses a different Tibetan as BuddhaNexus.
2. Polyglotta uses verse numbers, which are also used in parallel.json and not the numbers used in BuddhaNexus.
3. The Sanskrit Udanavarga numbers used in parallel.json are those used in BuddhaNexus.
4. The Sanskrit Udanavarga can vary slightly in parallel.json from the version used in BuddhaNexus due to some differences in spacing, etc. But the numbers are the same.

Explanation of parallel.json: NOTE: in parallel_array.json this has all been spelled out in the same arrays that are used in BuddhaNexus backend jsons.

Most objects in parallel.json look like this:

  "1.01": {
    "S10udanav_u:uv_1.1_0-1": "stīnamiddhaṁ vinodyeha saṁpraharṣya ca mānasam | śṛṇutemaṁ pravakṣyāmi udānaṁ jinabhāṣitam ||",
    "uv-kg1#1": "|| rgyal bas ched du brjod gsuṅs pa || bdag gis rab tu bśad par bya || gñid daṅ rmugs pa rnams sol la || yid la dga’ ba bskyed de ñon ||"
  },

The number `1.01` is simply there to make sure that the items stay in the right order.
"S10udanav_u:uv_1.1_0-1" = the segment numbers as in BuddhaNexus. Although sometimes only one segment is shown here, most of the time these represent a range of segments. Here it is ["S10udanav_u:uv_1.1_0", "S10udanav_u:uv_1.1_1"]. In some cases there is a third part to this range when three or more segment numbers are grouped together to match the verse.
"uv-kg1#1": Polyglotta verse number.

Some objects look like this:

  "15.15a": {
    "S10udanav_u:uv_15.15a_0-1": "suprabuddham prabudhyante;ime gautama śrāvakāḥ | yeṣām divā ca rātrau ca nityam samādhayaḥ smṛtāḥ ||",
    "uv-kg15#316": "gaṅ źig ñin daṅ mtshan rnams su || rtag tu tiṅ ’dzin bźi dran pa || gau ta ma yi ñan thos de || legs par sad pas sad par gyur ||"
  }

Here the segment number "S10udanav_u:uv_15.15a_0-1" represents the range ["S10udanav_u:uv_15.15a_0","S10udanav_u:uv_15.15a_1"]. Basically similar as above but this is a alternative reading to "S10udanav_u:uv_15.15"

  "19.07": {
    "S10udanav_u:uv_19.7_0-a_1": "yo hy aśvam damayej jānyam ājāneyam ca saindhavam / kuñjaram vā mahā nāgam ātmā dāntas tato varam // yac ca iha aśvataram damayed ājanyam vā api saindhavam / kuñjaram vā mahā nāgam ātma dāntas tato varam //",
    "uv-kg19#393": "glaṅ po’i naṅ na glaṅ chen daṅ || sin du’i caṅ śes rta daṅ ni || dre’u ’dul byed pa gaṅ yin pa || de bas bdag ñid ’dul ba mchog ||"
  },

This means that "S10udanav_u:uv_19.7_0-a_1" = ["S10udanav_u:uv_19.7_0","S10udanav_u:uv_19.7_1","S10udanav_u:uv_19.7_a_0","S10udanav_u:uv_19.7_a_1"]

  "5.16a": {
    "S10udanav_u:uv_5.16_1": "yathā pratyanta nagaram guptam antar bahisthiram | [antar bahiḥ sthiram]",
    "uv-kg5#136ab": "dper na dgon pa’i groṅ khyer dag || phyi naṅ sruṅ bar byed pa ltar ||"
  },
  "5.17": {
    "S10udanav_u:uv_5.17_0-1": "evam gopayata ātmānam kṣaṇo vo mā hy upatyagāt | kṣaṇa atītā hi śocante narakeṣu samarpitāḥ ||",
    "uv-kg5#136cdef": "dal ’byor chud ni mi zos pa || de ltar bdag ni bsruṅ bar bya || sems can dmyal bar skye na yaṅ || dal ’byor thal bas ’gyod par ’oṅ ||"
  },

In this case the one segment "S10udanav_u:uv_5.16_1" matches only part of the tibetan verse 136, namely the first two lines, which is marked by "uv-kg5#136ab". The last 4 lines of the tibetan verse match the entire verse "S10udanav_u:uv_5.17_0-1" = ["S10udanav_u:uv_5.17_0","S10udanav_u:uv_5.17_1"] = "uv-kg5#136cdef"


In some cases there is an overlap i.e. one verse has multiple parallels in the other text.
