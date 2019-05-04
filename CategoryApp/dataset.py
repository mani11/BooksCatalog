from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import BookCategory, Base, User, Books

engine = create_engine('sqlite:///books.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Category

category1 = BookCategory(name="Fiction")
session.add(category1)
session.commit()

category2 = BookCategory(name="Non Fiction")
session.add(category2)
session.commit()

category3 = BookCategory(name="Cookbooks")
session.add(category3)
session.commit()

category4 = BookCategory(name="History")
session.add(category4)
session.commit()

category5 = BookCategory(name="Literature")
session.add(category5)
session.commit()


# Books for category fiction

Book1 = Books(name="1984", author="George Orwell", description="Among the seminal texts of the 20th century, Nineteen Eighty Four is a rare work that grows more haunting as its futuristic purgatory becomes more real. Published in 1949, the book offers political satirist.", price='$4.00', category_id=1, user_id=1)
session.add(Book1)
session.commit()

Book2 = Books(name="A tale of two cities", author="Charles Dickens", description="After eighteen years as a political prisoner in the Bastille, the ageing Doctor Manette is finally released and reunited with his daughter in England. There the lives of two very different men, Charles Darnay, an exiled French aristocrat, and Sydney Carton, a disreputable but brilliant English lawyer, become enmeshed through their love for Lucie Manette. From the tranquil roads of London, they are drawn against their will to the vengeful, bloodstained streets of Paris at the height of the Reign of Terror, and they soon fall under the lethal shadow of La Guillotine.", price='$4.00', category_id=1, user_id=1)
session.add(Book2)
session.commit()

Book3 = Books(name="The Paying Guests", author="Sarah Waters", description=" A psychological and dramatic tour de force from beloved international bestseller Sarah Waters. The year is 1922, and London is tense. Ex-servicemen are disillusioned, the out of work and the hungry are demanding change", price='$4.00', category_id=1, user_id=1)
session.add(Book3)
session.commit()

# Books for category Non Fiction

Book4 = Books(name="Atomic Habits", author="James Clear", description="No matter your goals, Atomic Habits offers a proven framework for improving--every day. James Clear, one of the world's leading experts on habit formation, reveals practical strategies that will teach you exactly how to form good habits, break bad ones, and master the tiny behaviors that lead to remarkable results.", price='$4.00', category_id=2, user_id=1)
session.add(Book4)
session.commit()

Book5 = Books(name="Sapiens", author="Yuval Noah Harari", description="In Sapiens, Dr Yuval Noah Harari spans the whole of human history, from the very first humans to walk the earth to the radical and sometimes devastating breakthroughs of the Cognitive, Agricultural and Scientific Revolutions.", price='$4.00', category_id=2, user_id=1)
session.add(Book5)
session.commit()

Book6 = Books(name="David and Goliath", author="Malcolm Gladwell", description="Now he looks at the complex and surprising ways the weak can defeat the strong, the small can match up against the giant, and how our goals (often culturally determined) can make a huge difference in our ultimate sense of success. Drawing upon examples from the world of business, sports, culture, cutting-edge psychology, and an array of unforgettable characters around the world, David and Goliath is in many ways the most practical and provocative book Malcolm Gladwell has ever written.", price='$4.00', category_id=2, user_id=1)
session.add(Book6)
session.commit()

# Books for category Cookbooks

Book7 = Books(name="Japanese Soul Cooking", author="Tadashi Ono,  Harris Salat", description="It is time for gyoza, curry, tonkatsu, and furai. These icons of Japanese comfort food cooking are the dishes you will find in every kitchen and street corner hole in the wall restaurant in Japan.", price='$4.00', category_id=3, user_id=1)
session.add(Book7)
session.commit()

Book8 = Books(name="Deepa's Secret", author="Deepa Thomas", description="Part Indian cookbook, diet book, kitchen companion, and memoir, Deepas Secrets introduces breakthrough slow carb and gut-healing recipes that are simple, healthy, and nutrient-packed, without sacrificing its rich South Asian flavors. On a mission to demystify an exotic cuisine, Thomas provides step by step recipes with ingredient substitutions, shortcuts, and secret techniques that will make New Indian easy, everyday fare.", price='$4.00', category_id=3, user_id=1)
session.add(Book8)
session.commit()

Book9 = Books(name="Mangolia Table", author="Joanna Gaines", description="Jo believes there is no better way to celebrate family and friendship than through the art of togetherness, celebrating tradition, and sharing a great meal. Magnolia Table includes 125 classic recipes from breakfast, lunch, and dinner to small plates, snacks, and desserts presenting a modern selection of American classics and personal family favorites. Complemented by her love for her garden, these dishes also incorporate homegrown, seasonal produce at the peak of its flavor. Inside Magnolia Table, you will find recipes the whole family will enjoy.", price='$4.00', category_id=3, user_id=1)
session.add(Book9)
session.commit()

# Books for category History

Book10 = Books(name="Out of China", author="Robert Bickers", description="Out of China uses a brilliant array of unusual, strange and vivid sources to recreate a now fantastically remote world: the corrupt, lurid modernity of pre War Shanghai, the often tiny patches of extra territorial land controlled by European powers , the entrepots of Hong Kong and Macao, and the myriad means, through armed threats, technology and legal chicanery, by which China was kept subservient.", price='$4.00', category_id=4, user_id=1)
session.add(Book10)
session.commit()

Book11 =  Books(name="The First World War", author="John Keegan", description="Probing the mystery of how a civilization at the height of its achievement could have propelled itself into such a ruinous conflict, Keegan takes us behind the scenes of the negotiations among Europe's crowned heads and ministers, and their doomed efforts to defuse the crisis. He reveals how, by an astonishing failure of diplomacy and communication, a bilateral dispute grew to engulf an entire continent.", price='$4.00', category_id=4, user_id=1)
session.add(Book11)
session.commit()

Book12 = Books(name="Rites of Spring", author="Modris Eksteins", description="Dazzling in its originality, Rites of Spring probes the origins, impact, and aftermath of World War one, from the premiere of Stravinskys ballet The Rite of Spring in 1913 to the death of Hitler in 1945. Recognizing that The Great War was the psychological turning point for modernism as a whole, author Modris Eksteins examines the lives of ordinary people, works of modern literature, and pivotal historical events to redefine the way we look at our past and toward our future.", price='$4.00', category_id=4, user_id=1)
session.add(Book12)
session.commit()

# Books for category Literature

Book13 = Books(name="The Great Gatsby", author="F. Scott Fitzgerald", description="THE GREAT GATSBY, F. Scott Fitzgerald's third book, stands as the supreme achievement of his career. This exemplary novel of the Jazz Age has been acclaimed by generations of readers. The story is of the fabulously wealthy Jay Gatsby and his new love for the beautiful Daisy Buchanan, of lavish parties on Long Island at a time when The New York Times noted 'gin was the national drink and sex the national obsession,' it is an exquisitely crafted tale of America in the 1920s.", price='$4.00', category_id=5, user_id=1)
session.add(Book13)
session.commit()

Book14 = Books(name="To Kill a Mockingbird", author="Harper Lee", description="Compassionate, dramatic, and deeply moving, To Kill A Mockingbird takes readers to the roots of human behavior - to innocence and experience, kindness and cruelty, love and hatred, humor and pathos. Now with over 18 million copies in print and translated into forty languages, this regional story by a young Alabama woman claims universal appeal. Harper Lee always considered her book to be a simple love story. Today it is regarded as a masterpiece of American literature.", category_id=5, user_id=1, price='$4.00')
session.add(Book14)
session.commit()

Book15 = Books(name="Hamlet", author="William Shakespeare",
               description="Among Shakespeare's plays, 'Hamlet'"
               "is considered by many his masterpiece. Among actors,"
               "the role of Hamlet, Prince of Denmark,"
               "is considered the jewel in the crown of a triumphant"
               "theatrical career. Now Kenneth Branagh plays the leading"
               "role and co-directs a brillant ensemble performance."
               "Three generations of legendary leading actors, many of"
               "whom first assembled for the Oscar-winning film 'Henry V',"
               "gather here to perform the rarely heard complete version of the play."
               "This clear, subtly nuanced, stunning dramatization, presented by"
               "The Renaissance Theatre Company in association with 'Bbc' 
               "Broadcasting,features such luminaries as Sir John Gielgud, Derek Jacobi,"
               " Emma Thompson and Christopher Ravenscroft. It combines a full"
               " cast with stirring music and sound effects to bring this magnificent"
               " Shakespearen classic vividly to life. Revealing new riches with each"
               " listening, this production of 'Hamlet' is an invaluable aid for students,"
               "teachers and all true lovers of Shakespeare - a recording to be"
               " treasured for decades to come", price='$4.00', category_id=5, user_id=1)
session.add(Book15)
session.commit()

print "Added Books!!"
