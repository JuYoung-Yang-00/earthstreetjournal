import 'package:flutter/material.dart';
import 'components/footer.dart';

import 'package:flutter_animate/flutter_animate.dart';

import 'dart:math' as math;

import 'components/categoryHeader.dart';

import 'components/colors.dart';

class LandingPage extends StatefulWidget {
  const LandingPage({super.key, required this.title});

  final String title;

  @override
  State<LandingPage> createState() => _LandingPageState();
}

class _LandingPageState extends State<LandingPage> {
  List<String> WSJHeadlines = [];
  List<String> WSJSubHeadlines = [];
  List<String> WSJImageLinks = [];
  List<String> WSJArticleLinks = [];

  @override
  void initState() {
    super.initState();
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverList(
            delegate: SliverChildListDelegate([
              const SizedBox(height: 25.0),
              Padding(
                padding: const EdgeInsets.fromLTRB(35.0, 0, 35.0, 0),
                child: Row(
                  children: [
                    // This Expanded widget contains the centered content.
                    Expanded(
                      child: Center(
                        child: Material(
                          color: Colors.transparent,
                          child: InkWell(
                            onTap: () async {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => const LandingPage(
                                      title: 'refreshed landing page'),
                                ),
                              );
                            },
                            splashColor: Colors.transparent,
                            highlightColor: Colors.transparent,
                            hoverColor: Colors.transparent,
                            child: Animate(
                              // Assuming Animate is a custom widget in your app
                              effects: const [
                                FadeEffect(duration: Duration(seconds: 1)),
                              ],
                              child: const Text(
                                "Earth Street Journal",
                                style: TextStyle(
                                  fontFamily: 'Edensor',
                                  fontSize: 60,
                                  color: AppColors.esjBlack,
                                  fontWeight: FontWeight.w500,
                                  letterSpacing: 3,
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                    // Login button to the extreme right
                    // Replace this container with your actual login button
                    GestureDetector(
                      onTap: () async {
                        // Action to be performed when the button is clicked
                        setState(() {
                          //buttonPressed = true;
                        });

                        //await Future.delayed(const Duration(milliseconds: 200));

                        //Navigator.of(context).push(
                        // 09.17.2023 (SUN) - BASICALLY THIS, BUT GOING INTO LOGIN PAGE FOR THAT SPECIFIC SCHOOL
                        // 10.02.2023 (MON) - working on this now - we're going to type_school_id.dart from here

                        //MaterialPageRoute(
                        //builder: (context) => TypeSchoolIdPage(
                        //schoolName: widget.schoolName,
                        //),
                        //),
                        //);
                      },
                      child: SizedBox(
                        width: 90.0,
                        child: Material(
                          color: Colors.transparent,
                          elevation:
                              0.0, // Set the elevation for the shadow effect
                          shadowColor: Colors.transparent,
                          borderRadius: BorderRadius.circular(
                              23.0), // Set the border radius for the button
                          child: Ink(
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(23.0),
                                border: Border.all(
                                  color: AppColors.esjBlack, // Specify color
                                  width: 1.0, // Specify width
                                  style: BorderStyle.solid, // Specify style
                                  // strokeAlign: BorderSide.strokeAlignInside, // Optional: Uncomment if needed
                                ),
                              ),
                              child: Column(
                                children: const [
                                  SizedBox(height: 7.0),
                                  Text(
                                    //'Looking for ${user.lookingFor}',
                                    "Login",

                                    style: TextStyle(
                                      fontFamily: 'Thonburi',
                                      fontSize: 14,
                                      color: AppColors.esjBlack,
                                    ),
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                  SizedBox(height: 7.0),
                                ],
                              )),
                        ),
                      ),
                    )
                  ],
                ),
                //login button
              ),
              const SizedBox(height: 15.0),
              Container(
                height: 0.8, // Adjust the height to make the line thicker
                color: const Color(0xff282C32), // Color of the line
                child: const Divider(
                  color: Colors
                      .transparent, // Set the color of the Divider to transparent
                  height: 0,
                  thickness: 0,
                ),
              ),
              const SizedBox(height: 5),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: const [
                  CategoryHeader(
                      title: 'Science',
                      selected: false,
                      goesTo: LandingPage(title: 'home')),
                  SizedBox(width: 11.0),
                  CategoryHeader(
                      title: 'Nature',
                      selected: false,
                      goesTo: LandingPage(title: 'home')),
                  SizedBox(width: 11.0),
                  /*
                  CategoryHeader(
                      title: 'Energy',
                      selected: false,
                      goesTo: LandingPage(title: 'home')),
                      */
                  //SizedBox(width: 11.0),
                  CategoryHeader(
                      title: 'Home',
                      selected: true,
                      goesTo: LandingPage(title: 'home')),
                  SizedBox(width: 11.0),
                  CategoryHeader(
                      title: 'Politics',
                      selected: false,
                      goesTo: LandingPage(title: 'home')),
                  SizedBox(width: 11.0),
                  /*
                  CategoryHeader(
                      title: 'Business',
                      selected: false,
                      goesTo: LandingPage(title: 'home')),
                      */
                  //SizedBox(width: 11.0),
                  CategoryHeader(
                      title: 'Tech',
                      selected: false,
                      goesTo: LandingPage(title: 'home')),
                  SizedBox(width: 11.0),
                ],
              ),
              const SizedBox(height: 5),
              Container(
                height: 0.8, // Adjust the height to make the line thicker
                color: const Color(0xff282C32), // Color of the line
                child: const Divider(
                  color: Colors
                      .transparent, // Set the color of the Divider to transparent
                  height: 0,
                  thickness: 0,
                ),
              ),
            ]),
          ),
          SliverFillRemaining(
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.center,
                //mainAxisAlignment: MainAxisAlignment,
                children: [
                  SizedBox(height: 35.0),
                  SizedBox(height: 35.0),
                  SizedBox(height: 35.0),
                  SizedBox(height: 35.0),
                  SizedBox(height: 35.0),
                  FooterComponent(title: "footer"),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
