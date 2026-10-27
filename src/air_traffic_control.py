EPS = 1e-6

def is_equal(x, y):
    """Return True when x and y should be treated as equal."""
    return abs(x - y) <= EPS


def is_less(x, y):
    """Return True when x is definitely smaller than y."""
    return x < y - EPS

def is_greater(x, y):
    """Return True when x is definitely greater than y."""
    return x > y + EPS
    
def is_less_equal(x, y):
    """Return True when x should be treated as less than or equal to y."""
    return not is_greater(x, y)
    
def is_greater_equal(x, y):
    """Return True when x should be treated as greater than or equal to y."""
    return not is_less(x, y)
def quadratic(a,b,c):
    time_list=[]
    if is_greater_equal(b**2-4*a*c,0)==False:
        return []
    elif is_equal(a,0)==True:
        if is_equal(b,0)!=True:
            r=-c/b
            if is_greater_equal(r,0):
                return [r]
        return []
    else:
        d=(b**2-4*a*c)**(0.5)
        r1=(-b+d)/(2*a)
        r2=(-b-d)/(2*a)
        m=min(r1,r2)
        if is_greater_equal(m,0)==True:
            time_list.append(m)
        if is_greater_equal(r1+r2-m,0)==True:
            time_list.append(r1+r2-m)
        return time_list
def tuple_multiplier(multiplier,tuple):
    ans=()
    for i in tuple:
        ans+=(i*multiplier,)
    return ans
def tuple_addition(a,b):
    ans=()
    for i in range(len(a)):
        ans+=(a[i]+b[i],)
    return ans
def speed_time(v,a,max,t):
    a1=a[0]**2+a[1]**2+a[2]**2
    b=2*a[0]*v[0]+2*a[1]*v[1]+2*a[2]*v[2]
    c=v[0]**2+v[1]**2+v[2]**2-max**2
    if is_equal(a1,0):
        return -1
    if is_equal(c,0):
        if is_greater(b,0):
            return 0
        else:
            return -b/a1
    tl=quadratic(a1,b,c)
    if len(tl)>=1:
        tr=tl[0]
    else:
        tr=-1
    if tr!=-1 and is_less(tr,t):
        return tr
    return -1
def landing_checker(a,v,z):
    stat1=True
    for i in a:
        if is_equal(i,0)!=True:
            stat1=False
    for i in v:
        if is_equal(i,0)!=True:
            stat1=False
    if is_equal(z,0)!=True:
        stat1=False
    return stat1
def crash_time(a,v,p,t):
    tl=quadratic(a/2,v,p)
    return tl
def crash_check(t,v,a):
    v_impact=tuple_addition(v,tuple_multiplier(t,a))
    if is_less(v_impact[-1],0)==True:
        return True
    if is_less(a[-1],0):
        return True
    return False
def collision_time(l1,l2,t_ava):
    #list_format=[time,max_speed,position,velocity,(0,0,0),"flying"]
    acc1=l1[-2]
    acc2=l2[-2]
    a1=(acc1[0]-acc2[0])/2
    a2=(acc1[1]-acc2[1])/2
    a3=(acc1[2]-acc2[2])/2
    v1=l1[3]
    v2=l2[3]
    b1=v1[0]-v2[0]
    b2=v1[1]-v2[1]
    b3=v1[2]-v2[2]
    p1=l1[2]
    p2=l2[2]
    c1=p1[0]-p2[0]
    c2=p1[1]-p2[1]
    c3=p1[2]-p2[2]
    if is_equal(c1,0)!=True:
        a=a1
        b=b1
        c=c1
    elif is_equal(c2,0)!=True:
        a=a2
        b=b2
        c=c2
    elif is_equal(c3,0)!=True:
        a=a3
        b=b3
        c=c3
    else:
        return 0
    tl=quadratic(a,b,c)
    for t in tl:
        change_pos_1=tuple_addition(tuple_multiplier(t,v1),tuple_multiplier(0.5*((t)**2),(acc1)))
        pos_1=tuple_addition(p1,change_pos_1)
        change_pos_2=tuple_addition(tuple_multiplier(t,v2),tuple_multiplier(0.5*((t)**2),(acc2)))
        pos_2=tuple_addition(p2,change_pos_2)
        state_collision=True
        for i in range(3):
            if is_equal(pos_1[i],pos_2[i])!=True:
                state_collision=False
        if state_collision==True and is_less_equal(t,t_ava):
            return t
    return -1
def updater(dic,time):
    #list_format=[time,max_speed,position,velocity,acc,"flying"]
    for i in dic:
        f=dic[i]
        t=time-f[0]
        change_pos=tuple_addition(tuple_multiplier(t,f[3]),tuple_multiplier(0.5*((t)**2),(f[-2])))
        f[2]=tuple_addition(f[2],change_pos)
        f[3]=tuple_addition(f[3],tuple_multiplier(t,f[-2]))
        f[0]=time
    return dic
def operator(dic,time):
    for i in dic:
        f=dic[i]
        if landing_checker(f[-2],f[3],f[2][-1])==True:
            dic[i][-1]="landed safely"
    l=[]
    l1=[]
    for i in dic:
        t_ava=time-dic[i][0]
        for j in dic:
            if j!=i:
                t=collision_time(dic[i],dic[j],t_ava)
                if t!=-1:
                    l1.append([t,i,j])
    for i in dic:
        f=dic[i]
        t_ava=time-dic[i][0]
        acc=f[-2]
        p=f[2]
        v=f[3]
        max=f[1]
        t1=speed_time(v,acc,max,t_ava)
        if t1!=-1 and is_less(t1,t_ava):
            l.append([t1,i])
        tl=crash_time(acc[-1],v[-1],p[-1],t_ava)
        for t in tl:
            if is_less_equal(t,t_ava)==True:
                if crash_check(t,v,acc)==True:
                    l.append([t,i])
    l.sort()
    l1.sort()
    i=0
    j=0
    last_time=-1
    while i<len(l) or j<len(l1):
        if i!=len(l) and (j==len(l1) or is_less_equal(l[i][0],l1[j][0])):
            id=l[i][-1]
            if dic[id][-1]=='flying':
                dic[id][-1]='accident'
            i+=1
        else:
            current_time=l1[j][0]
            if is_equal(current_time,last_time)!=True:
                condition={}
                for i1 in dic:
                    condition[i1]=dic[i1][-1]
                last_time=current_time
            id1=l1[j][1]
            id2=l1[j][2]
            if condition[id1]=="flying" and condition[id2]=='flying':
                dic[id1][-1]='accident'
                dic[id2][-1]='accident'
            j+=1
    dic=updater(dic,time)
    return dic
    
class Flight:
    """A single aircraft."""
    def __init__(self, max_speed, position, velocity):
        """
        max_speed : int, the highest speed this flight may hold
        position : a tuple (x, y, z) of integers, where it starts
        velocity : a tuple (vx, vy, vz) of integers, its initial velocity
        
        A newly created flight has the given initial velocity and acceleration
        (0, 0, 0). Its status must already be correct at the moment it is
        created.
        """
        self.max_speed=max_speed
        self.pos=position
        self.v=velocity
        self.t=0
        self.a=(0,0,0)
        self.landed=False
        self.accident=False
        if is_less(self.pos[-1],0)==True:
            self.accident=True
        mod=0
        for i in self.v:
            mod+=i**2
        if is_greater(mod,self.max_speed**2):
            self.accident=True
    def set_acceleration(self, time, acceleration):
        """
        time : the instant from which the new acceleration applies
        acceleration : a tuple (ax, ay, az) of integers
        
        A flight that has already finished ignores this instruction.
        """
        change_pos=tuple_addition(tuple_multiplier((time-self.t),(self.v)),tuple_multiplier(0.5*((time-self.t)**2),(self.a)))
        p1=tuple_addition(self.pos,change_pos)
        v1=tuple_addition(self.v,tuple_multiplier(time-self.t,self.a))
        if self.accident==False and self.landed==False:
            t1=speed_time(self.v,self.a,self.max_speed,time-self.t)
            if t1!=-1 and is_less(t1,time-self.t):
                self.accident=True
            self.landed=landing_checker(self.a,v1,p1[2])
        if self.accident==False and self.landed==False:
            tl=crash_time(self.a[2],self.v[2],self.pos[2],time-self.t)
            for t in tl:
                if is_less_equal(t,time-self.t)==True:
                    self.accident=crash_check(t,self.v,self.a)
        if self.accident==False and self.landed==False:
            self.pos=p1
            self.v=v1
            self.t=time
            self.a=acceleration
    def status(self, time):
        """
        Return this flight’s status at the given instant: "flying",
        "accident" or "landed safely".
        """
        v1=tuple_addition(self.v,tuple_multiplier(time-self.t,self.a))
        if self.accident==False and self.landed==False:
            t1=speed_time(self.v,self.a,self.max_speed,time-self.t)
            if t1!=-1 and is_less(t1,time-self.t):
                self.accident=True
            self.landed=landing_checker(self.a,v1,self.pos[2])
        if self.accident==False and self.landed==False:
            tl=crash_time(self.a[2],self.v[2],self.pos[2],time-self.t)
            for t in tl:
                if is_less_equal(t,time-self.t)==True:
                    self.accident=crash_check(t,self.v,self.a)
        if self.landed==True:
            return  "landed safely"
        if self.accident==True:
            return "accident"
        return "flying"
class AirTrafficControl:
    """The controller, which owns every flight."""

    def __init__(self):
        """Start a new session, with no flights, at time 0."""
        self.dic_original={}

    def create(self, time, flight_id, max_speed, position, velocity):
        """Create a flight with the given position and initial velocity."""
        #list_format=[time,max_speed,position,velocity,(0,0,0),"flying"]
        dic=operator(self.dic_original,time)
        dic[flight_id]=[time,max_speed,position,velocity,(0,0,0),"flying"]
        f=dic[flight_id]
        if is_less(f[2][-1],0)==True:
            dic[flight_id][-1]='accident'
        mod=0
        for i in  f[3]:
            mod+=i**2
        if is_greater(mod,f[1]**2):
            dic[flight_id][-1]='accident'
        if landing_checker(f[-2],f[3],f[2][-1])==True:
                dic[flight_id][-1]="landed safely"
        for i in dic:
            if i!=flight_id:
                collision_stat=True
                for j in range(3):
                    if is_equal(dic[i][2][j],dic[flight_id][2][j])!=True:
                        collision_stat=False
                if collision_stat==True:
                    if dic[i][-1]=='flying' and dic[flight_id][-1]=='flying':
                        dic[i][-1]='accident'
                        dic[flight_id][-1]='accident'
        self.dic_original=dic

    def update(self, time, flight_id, acceleration):
        """Send an acceleration instruction to a flight at the given instant."""
        self.dic_original=operator(self.dic_original,time)
        if flight_id in self.dic_original:
            self.dic_original[flight_id][-2]=acceleration

    def status(self, time, flight_id):
        """
        Return the status of the given flight at the given instant: "flying",
        "accident", "landed safely", or "does not exist" if no flight with
        that identifier has ever been created.
        """
        self.dic_original=operator(self.dic_original,time)
        if flight_id in self.dic_original:
            return self.dic_original[flight_id][-1]
        else:
            return 'does not exist'
