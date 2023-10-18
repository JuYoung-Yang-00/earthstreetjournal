//import 'dart:ui';

import 'package:flutter/material.dart';

import 'dart:math' as math;
import 'dart:async';
import 'dart:ui';

import 'package:url_launcher/url_launcher.dart';

import 'package:flutter_animate/flutter_animate.dart';

class FooterComponent extends StatefulWidget {
  const FooterComponent({super.key, required this.title});

  final String title;

  @override
  State<FooterComponent> createState() => _FooterComponentState();
}

class _FooterComponentState extends State<FooterComponent> {
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
    return SafeArea(
      child: Column(
        children: [
          Column(
            children: [
              const SizedBox(height: 30.0),
              Animate(
                  effects: const [
                    FadeEffect(duration: Duration(seconds: 1)),
                  ],
                  child: SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: Row(
                      children: [
                        Padding(
                          padding: const EdgeInsets.fromLTRB(35, 0, 35, 0),
                          child: Row(
                            children: [
                              Text(
                                "© 20xx Made by ".replaceAll(
                                    "20xx", DateTime.now().year.toString()),
                                style: const TextStyle(
                                  fontFamily: 'Thonburi',
                                  fontSize: 13,
                                  color: Color(0xff272C32),
                                  fontWeight: FontWeight.normal,
                                  letterSpacing: 1.5,
                                ),
                              ),
                              Material(
                                color: Colors.transparent,
                                child: InkWell(
                                  onTap: () async {
                                    Uri _url = Uri.parse(
                                        'https://www.linkedin.com/in/juyoung-yang/');
                                    if (!(await launchUrl(_url))) {
                                      throw 'Could not launch $_url';
                                    }
                                  },
                                  splashColor: Colors.transparent,
                                  highlightColor: Colors.transparent,
                                  hoverColor: Colors.transparent,
                                  child: Animate(
                                    effects: const [
                                      FadeEffect(
                                          duration: Duration(seconds: 1)),
                                    ],
                                    child: const Text(
                                      "Justin Yang",
                                      style: TextStyle(
                                        fontFamily: 'Thonburi-Bold',
                                        fontSize: 13,
                                        color: Color(0xff00684b),
                                        fontWeight: FontWeight.normal,
                                        letterSpacing: 1.5,
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              const Text(
                                " and ",
                                style: TextStyle(
                                  fontFamily: 'Thonburi',
                                  fontSize: 13,
                                  color: Color(0xff272C32),
                                  fontWeight: FontWeight.normal,
                                  letterSpacing: 1.5,
                                ),
                              ),
                              Material(
                                color: Colors.transparent,
                                child: InkWell(
                                  onTap: () async {
                                    Uri _url = Uri.parse(
                                        'https://www.linkedin.com/in/wujehevankim/');
                                    if (!(await launchUrl(_url))) {
                                      throw 'Could not launch $_url';
                                    }
                                  },
                                  splashColor: Colors.transparent,
                                  highlightColor: Colors.transparent,
                                  hoverColor: Colors.transparent,
                                  child: Animate(
                                    effects: const [
                                      FadeEffect(
                                          duration: Duration(seconds: 1)),
                                    ],
                                    child: const Text(
                                      "Evan Kim",
                                      style: TextStyle(
                                        fontFamily: 'Thonburi-Bold',
                                        fontSize: 13,
                                        color: Color(0xff00684b),
                                        fontWeight: FontWeight.normal,
                                        letterSpacing: 1.5,
                                      ),
                                    ),
                                  ),
                                ),
                              ),
                              const Text(
                                " | Created with Flutter, Flask, MongoDB, Figma",
                                style: TextStyle(
                                  fontFamily: 'Thonburi',
                                  fontSize: 13,
                                  color: Color(0xff272C32),
                                  fontWeight: FontWeight.normal,
                                  letterSpacing: 1.5,
                                ),
                                softWrap: true,
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  )),
              const SizedBox(height: 30.0),
            ],
          ),
        ],
      ),
    );
  }
}
