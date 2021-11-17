def visit_length(visit):
    """
    This function is used to determine the length of a person's visit to
    a particular place
    visit_length(("Irene", "Skylabs", 3, 9, 15, 13, 45))
    (4, 30)
    """
    # converting arrive and leave time departed time to minutes
    arrive_time = int(visit[3]) * 60 + int(visit[4])
    leave_time = int(visit[5]) * 60 + int(visit[6])
    # measuring the time length
    time_length = leave_time - arrive_time
    if time_length <= 0:
        return None
    else:
        return (time_length // 60, time_length % 60)


def contact_event(visit_a, visit_b):
    """This function is used to determine whether two visits
    overlap in time and space

    :param visit_a: a 7-tuple containing data of person a's visit
    to a location
    :param visit_b: a 7-tuple containing data of person b's visit
    to a location
    :return: True if two visits overlap and False if not



    print(contact_event(('Russel', 'Foodigm', 2, 9, 0, 10, 0), ('Natalya', 'Foodigm', 2, 9, 30, 9, 45)))
    True
    """

    # calculating the arrive time, time length, leave time of person a in mins
    arrive_time_a = int(visit_a[3]) * 60 + int(visit_a[4])
    leave_time_a = int(visit_a[5]) * 60 + int(visit_a[6])
    time_length_a = leave_time_a - arrive_time_a

    # calculating the arrive time, time length, leave time of person b in mins
    arrive_time_b = int(visit_b[3]) * 60 + int(visit_b[4])
    leave_time_b = int(visit_b[5]) * 60 + int(visit_b[6])
    time_length_b = leave_time_b - arrive_time_b

    # Case 1: Invalid visits
    if time_length_b <= 0 or time_length_a <= 0:
        return None

    # Case 2: same person and different locations
    elif visit_a[0] == visit_b[0] or visit_a[1] != visit_b[1]:
        return False

    # Case 3: different day
    elif visit_a[2] != visit_b[2]:
        return False

    else:
        # check if the two visits overlap or not
        if arrive_time_b >= leave_time_a or leave_time_b <= arrive_time_a:
            return False
        return True


def potential_contacts(person_a, person_b):
    """
    This function identifies all of the potential contacts between two
    people, given data on their movement over multiple days.

    :param person_a: a list of 7-tuples containing data of
    person a's visit to a location

    :param person_b: a list of 7-tuples containing data of
    person b's visit to a location

    :return:  a tuple of
        answer_set: a set of potential contact locations
    and times in the form of 6-tuples
        answer_tup: a 2-tuple containing (hours, minutes)
    showing the total duration of potential contact

    potential_contacts([('Russel', 'Foodigm', 2, 9, 0, 10, 0), ('Russel', 'Afforage', 2, 10, 0, 11, 30), ('Russel', 'Nutrity', 2, 11, 45, 12, 0), ('Russel', 'Liberry', 3, 13, 0, 14, 15)], [('Chihiro', 'Foodigm', 2, 9, 15, 9, 30), ('Chihiro', 'Nutrity', 4, 9, 45, 11, 30), ('Chihiro', 'Liberry', 3, 12, 15, 13, 25)])
    ({('Foodigm', 2, 9, 15, 9, 30), ('Liberry', 3, 13, 0, 13, 25)}, (0, 40))
    """

    # answer_set is the returned set of the function
    answer_set = set()
    # duration is the duration between 2 people in contact in minutes
    duration = 0
    answer_tup = (0, 0)
    # Check for no visits
    if len(person_a) == 0 or len(person_b) == 0:
        return (answer_set, answer_tup)

    for data_a in person_a:
        for data_b in person_b:
            # Different location and day
            if data_a[1] != data_b[1] or data_a[2] != data_b[2]:
                continue
            # converting arriving and leaving time for person a and b in mins
            arrive_time_a = int(data_a[3]) * 60 + int(data_a[4])
            leave_time_a = int(data_a[5]) * 60 + int(data_a[6])
            arrive_time_b = int(data_b[3]) * 60 + int(data_b[4])
            leave_time_b = int(data_b[5]) * 60 + int(data_b[6])

            # lst is a sorted list according to arriving time, which contains
            # 2 tuples of arriving and leaving time of each person
            lst = []
            lst.append((arrive_time_a, leave_time_a))
            lst.append((arrive_time_b, leave_time_b))
            lst.sort()
            # start_time is the time at which 2 people started
            # being in contact
            start_time = lst[1][0]

            # checking if the 2 visits overlap
            if lst[0][1] <= start_time:
                return (answer_set, (0, 0))
            else:
                # departed time is the time at which 2 people stopped
                # being at the same location
                if lst[0][1] <= lst[1][1]:
                    departed_time = lst[0][1]
                else:
                    departed_time = lst[1][1]

                (answer_set.add((data_a[1], data_a[2], start_time // 60,
                                 start_time % 60, departed_time // 60, departed_time % 60)))
                duration += (departed_time - start_time)

    # (hour, min) tuple of duration
    answer_tup = (duration // 60, duration % 60)
    return (answer_set, answer_tup)


# a correct implementation of potential_contacts(person_a, person_b)
# do not delete this line!
# import libaries and datasets
from reference import potential_contacts


def forward_contact_trace(visits, index, day_time, second_order=False):
    """
    The function identifies all potential contacts of a detected index
    case that occurred after the time that they were detected

    :param visits: list of visits, each visit is a 7-tuple
    :param index: index case (name)
    :param day_time: the time when the index case was detected
    (day, hour, minute)
    :param second_order: a Boolean flag indicating whether
    second order contacts of the index case should be included

    :return target: sorted list of IDs of people who should be
    traced and asked to quarantine. (potential contacts)


>>> visits = [('Russel', 'Nutrity', 1, 5, 0, 6, 0),
           ('Russel', 'Foodigm', 2, 9, 0, 10, 0),
           ('Russel', 'Afforage', 2, 10, 0, 11, 30),
           ('Russel', 'Nutrity', 2, 11, 45, 12, 0),
           ('Russel', 'Liberry', 3, 13, 0, 14, 15),
           ('Natalya', 'Nutrity', 1, 5, 30, 6, 45),
           ('Natalya', 'Afforage', 2, 8, 15, 10, 0),
           ('Natalya', 'Nutrity', 4, 10, 10, 11, 45),
           ('Chihiro', 'Foodigm', 2, 9, 15, 9, 30),
           ('Chihiro', 'Nutrity', 4, 9, 45, 11, 30),
           ('Chihiro', 'Liberry', 3, 12, 15, 13, 25)]

>>> forward_contact_trace(visits, 'Russel', (1, 9, 0), second_order=True)
['Chihiro', 'Natalya']
    """

    # target (list) stores all potential contacts of the detected case
    target = []
    # will be explained later
    my_dict = {}

    # converting the time that the infected case was detected into minutes
    stamp = day_time[0] * 24 * 60 + day_time[1] * 60 + day_time[2]

    # name contains the name of other people except the index case
    name = []
    for data in visits:
        if data[0] not in name and data[0] != index:
            name.append(data[0])

    for person in name:
        # Filtering data as input for the function potential_contacts
        data_index = []
        data_other = []
        for data in visits:
            if data[0] == index:
                data_index.append(data)
            if data[0] == person:
                data_other.append(data)

        answer = potential_contacts(data_index, data_other)

        # Extract the time that 2 people started to become in touch
        # from answer(return value of the function) and check if
        # it's after the time that the index case was detected to add to target
        lst_set = list(answer[0])
        lst_set = sorted(lst_set, key=lambda x: (x[1], x[2], x[3]))
        if len(lst_set) != 0:
            for time in lst_set:
                if (time[1] * 24 * 60 + time[2] * 60 + time[3]) > stamp:
                    if person not in target:
                        target.append(person)
                        my_dict[person] = (time[1], time[2], time[3])
                # my_dict keeps track of the earliest contact (day,hour,minute)
                # between the index case and F1(those infected by the index
                # case), in which 'earliest' is achieved by function sorted

    if second_order:
        for key in my_dict:
            # f2 contains the second order contacts (F2)
            f2 = forward_contact_trace(visits, key, my_dict[key])
            # add second order contacts into the returned list, target
            for people in f2:
                if people != index and people not in target:
                    target.append(people)
    return sorted(target)


# a correct implementation of potential_contacts(person_a, person_b)
# do not delete this line!
from reference import potential_contacts


def backward_contact_trace(visits, index, day_time, window):
    """
    The function identifies the all potential sources of the specified
    index case's infection.

    :param visits: list of visits, each visit is a 7-tuple
    :param index: index case (name)
    :param day_time: the time when the index case was detected
    (day, hour, minute)
    :param window: the number of days prior to the detection of
    the index case that backward tracing will be carried out

    :return target: alphabetically sorted list of IDs of people
    who might be the potential source of the index caes's infection

>>> visits = [('Russel', 'Foodigm', 2, 9, 0, 10, 0),
           ('Russel', 'Afforage', 2, 10, 0, 11, 30),
           ('Russel', 'Nutrity', 2, 11, 45, 12, 0),
           ('Russel', 'Liberry', 3, 13, 0, 14, 15),
           ('Natalya', 'Afforage', 2, 8, 15, 10, 0),
           ('Natalya', 'Nutrity', 4, 10, 10, 11, 45),
           ('Chihiro', 'Foodigm', 2, 9, 15, 9, 30),
           ('Chihiro', 'Nutrity', 4, 9, 45, 11, 30),
           ('Chihiro', 'Liberry', 3, 12, 15, 13, 25)]

>>> backward_contact_trace(visits, 'Natalya', (4, 13, 0), 1)
['Chihiro']
    """
    # create a time interval in minutes: (stamp_lower, stamp_higher) in
    # which the function can identify those who should be traced

    stamp_lower = (day_time[0] - window + 1) * 1440  # beginning of the day
    stamp_higher = (day_time[0]) * 1440 + day_time[1] * 60 + day_time[2]

    # target (list) stores all potential contacts of the detected case
    target = []
    # name contains the name of other people except the index case
    name = []
    for data in visits:
        if data[0] not in name and data[0] != index:
            name.append(data[0])

    for person in name:
        # Filtering data as input for the function potential_contacts
        data_index = []
        data_other = []
        for data in visits:
            if data[0] == index:
                data_index.append(data)
            if data[0] == person:
                data_other.append(data)

        answer = potential_contacts(data_index, data_other)
        # Extract the time that 2 people started to become in touch
        # from answer(return value of the function) and check if
        # it's within the interval to add to list: target
        lst_set = list(answer[0])
        if len(answer[0]) != 0:
            for time in lst_set:
                start_time = time[1] * 1440 + time[2] * 60 + time[3]
                if stamp_lower <= start_time < stamp_higher:
                    # avoid adding same name multiple times
                    if person not in target:
                        target.append(person)
    return sorted(target)



