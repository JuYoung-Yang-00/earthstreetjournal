/*


Center(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 1.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    SizedBox(
                      width: 90.0,
                      child: TextFormField(
                        controller: netId,
                        //focusNode: netIdFocusNode,
                        decoration: const InputDecoration(
                          hintText: "Email",
                          hintStyle: TextStyle(fontSize: 13.0),
                        ),
                        onChanged: (value) {
                          setState(() {
                            userNetId = value;
                            isButtonEnabled = userNetId.length > 2;
                          });
                        },
                      ),
                    ),
                    SizedBox(
                      width: 105.0,
                      child: Text(
                        schoolEmailAddressSuffix,
                        style: const TextStyle(
                          fontSize: 15.0,
                          color: Color.fromARGB(255, 78, 78, 78),
                          height: 1.9,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const Spacer(),
            Center(
                child: SizedBox(
              width: 250,
              //height: 35,
              child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    shape: const StadiumBorder(),
                    backgroundColor: isButtonEnabled ? beanGreen : Colors.grey,

                    foregroundColor: const Color(0xFF14D959),
                    //padding:const EdgeInsets.symmetric(horizontal: 26, vertical: 10),
                    elevation: 1,
                  ),
                  onPressed: () async {
                    final fetchedUser =
                        (await UserSheetsApi.getById(netId.text.trim()));
                    if (netId.text.trim().length <= 2) {
                      //nothing
                    } else {
                      if (netId.text.trim().length > 2 &&
                          (fetchedUser == null)) {
                        // NEW USER CASE
                        // create and add a new user that is that netid and
                        // everything else as default
                        /*
                      _user = User(
                        id: netId.text,
                        pw: 'samplePW',
                        imagePath: 'assets/profileBeans/profileBean1.png',
                        name: netId.text,
                        email: '${netId.text}@duke.edu',
                        about: '...',
                        diet: '...',
                        allergies: '...',
                        ethnicity: '...',
                        job: '...',
                        languages: '...',
                        mobility: '...',
                        neurodiversity: '...',
                        religion: '...',
                        sexuality: '...',
                        age: '...',
                        city: '...',
                        pronouns: '...',
                        instagram: '...',
                        linkedin: '...',
                        lookingFor: '...',
                        answer1: 'No preference        ',
                        answer2: 'All of the above',
                        answer3: 'No preference         ',
                        answer4: 'No preference     ',
                        answer5: 'No preference        ',
                        answer6: 'No preference          ',
                        answer7: 'No preference    ',
                        answer8: 'No preference',
                        answer9: 'No preference',
                      );
                      */

                        try {
                          //await UserSheetsApi.insert([_user!.toJson()]);

                          Navigator.of(context).pushReplacement(
                            MaterialPageRoute(
                              builder: (context) => SetPasswordPage(
                                theUserNetId: netId.text.trim(),
                              ),
                            ),
                          );
                        } catch (e) {
                          //print('Error updating user: $e');
                        }
                      } else {
                        //EXISTING USER CASE
                        //login as that user only is the password matches!
                        try {
                          //await UserSheetsApi.insert([_user!.toJson()]);

                          Navigator.of(context).pushReplacement(
                            MaterialPageRoute(
                              builder: (context) => LogInWithPasswordPage(
                                theUserNetId: netId.text.trim(),
                              ),
                            ),
                          );
                        } catch (e) {
                          //print('Error updating user: $e');
                        }
                      }
                    }

                    /*
                  try {
                    await UserSheetsApi.update(_user!.id, _user!.toJson());

                    Navigator.of(context).pushReplacement(
                      MaterialPageRoute(
                        builder: (context) => const MyHomePage(
                            title: 'back', selectedTabIndex: 2),
                      ),
                    );
                  } catch (e) {
                    //print('Error updating user: $e');
                  }
                  */
                  },
                  child: Column(
                    children: const [
                      SizedBox(height: 10.0),
                      Text(
                        "Select School",
                        style: TextStyle(
                          fontSize: 15.0,
                          color: AppColors.whiteText,
                        ),
                        overflow: TextOverflow.ellipsis,
                      ),
                      SizedBox(height: 10.0),
                    ],
                  )),
            )),



*/