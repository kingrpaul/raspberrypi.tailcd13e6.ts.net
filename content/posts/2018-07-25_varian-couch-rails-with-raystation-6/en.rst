====================================
Varian Couch Rails with Raystation 6
====================================
:date: 2018-07-25
:modified: 2026-10-08
:author: pairko
:category: post
:summary: Analysis of radiotherapy planning considerations using Raystation with the Varian Clinac.
:description: Analysis of radiotherapy planning considerations using Raystation with the Varian Clinac.
:tags: medical-physics
:slug: 2018-07-25_varian-couch-rails-with-raystation-6
:lang: en
:og_image: https://raspberrypi.tailcd13e6.ts.net/posts/2018-07-25_varian-couch-rails-with-raystation-6/social.jpg

Can we “shoot through the rails” of the Clinac iX when planning with RayStation?

Existing rules for handling the couch-top in Pinnacle planning and Varian delivery are as follows:

1. always treat using the imaging couch-top
2. never treat through the rails
3. never treat through the edge of the couch
4. except in special cases, use rails-in or rails-out; do not plan to adjust between beams
5. if treating through the couch

   * put the whole field through the couch
   * be cognizant of the bolus effect, ~½ cm equivalent
   * correct the MU for attenuation, 2-8%

.. figure:: /posts/2018-07-25_varian-couch-rails-with-raystation-6/fig11.png
   :width: 90 %
   :alt: 3D couch model
   :align: center

   Figure 1


.. figure:: /posts/2018-07-25_varian-couch-rails-with-raystation-6/fig21.png
   :width: 90 %
   :alt: 2D couch model with beams
   :align: center

   Figure 2


.. figure:: /posts/2018-07-25_varian-couch-rails-with-raystation-6/fig31.png
   :width: 50 %
   :alt: data table
   :align: center

   Figure 3


A Varian couch-top planning model is available, though from an unknown source. Direct use of this model does not integrate well with Pinnacle’s workflow. RayStation’s patient modeling tools are more sophisticated. This couch-top model was ported to RayStation and converted to a template, which can then be be workably applied to each patient.

Is this model, used with dosimetrically accurate?

During beam modeling, measurements were made using MapCheck, in it’s calibration sleeve, below 10 cm of plastic water. Detectors were at an effective depth of ~13 cm from the front and ~4 cm from the rear.

MapCheck was recalibrated and benchmark calculations and measurements were made using isocentric, AP, open, 20x20 fields.

.. figure:: /posts/2018-07-25_varian-couch-rails-with-raystation-6/fig4.png
   :width: 90 %
   :alt: screen shot
   :align: center

   Figure 4


Reasonable agreement was seen.

.. figure:: /posts/2018-07-25_varian-couch-rails-with-raystation-6/fig5.png
   :width: 90 %
   :alt: screen shot
   :align: center

   Figure 5


.. figure:: /posts/2018-07-25_varian-couch-rails-with-raystation-6/fig6.png
   :width: 90 %
   :alt: screen shot
   :align: center

   Figure 6


The same 20x20 beam was calculated and measured from the posterior.

.. figure:: /posts/2018-07-25_varian-couch-rails-with-raystation-6/fig7.png
   :width: 90 %
   :alt: screen shot
   :align: center

   Figure 7


Note that attenuation by the rails is on the order of 15%.

.. figure:: /posts/2018-07-25_varian-couch-rails-with-raystation-6/fig8.png
   :width: 90 %
   :alt: screen shot
   :align: center

   Figure 8


.. figure:: /posts/2018-07-25_varian-couch-rails-with-raystation-6/fig9.png
   :width: 90 %
   :alt: screen shot
   :align: center

   Figure 9


Findings
=========

1. Using this couch-top model does a ‘good job’ of predicting the magnitude of the disruption in     dose.
2. The rollers and clips, that are part of the couch top but are excluded from the model, produce a small     effect that can be ignored.
3. The rails close symmetrically and the rails-in model is symmetric. Yet, ~1 cm dose position error was seen     in the left rail. There is no machine readout of rail position and correctness depends on manual verification. Rail centering, adequate to achieve gamma-analysis “PASS”, requires some finesse.
4. CT-sim couch is fixed / centered and precisely planning for a non-centered couch ( lat ≠ 100 cm) is not straightforward. Indexing of immobilization is occasionally impractical and use of the lock-bar at the time of treatment is not machine-verified in any case. So, again, correctness depends on manual verification.

Conclusion
===========

1. When planning with generally maintain the existing rules. Do not routinely treat through the rails or couch edges.
2. Routinely apply the couch-top model in treatment planning. Use it to account for transmission through the couch and as an aid in avoiding the rails. Discontinue manual use of couch transmission factors.
3. Any intentional treatment through the rails is to be treated as a special procedure, cognizant of the real potential for meaningful dose placement errors.
4. Correctness of treatment dose continues to depend on manual verification.
