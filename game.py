import math
import os

class Thing:
    '''Fields: id (Nat),
               name (Str),
               description (Str)
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        
    def __repr__(self):
        return '<thing #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        
class Player:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               location (Room),
               inventory ((listof Thing))
    '''
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.location = None
        self.inventory = []
        
    def __repr__(self):
        return '<player #{0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.inventory) != 0:
            print('Carrying: {0}.'.format(
                ', '.join(map(lambda x: x.name,self.inventory))))
 
class Room:
    '''Fields: id (Nat),
               name (Str), 
               description (Str),
               contents ((listof Thing)),
               exits ((listof Exit))
    '''    
    
    def __init__(self, id):
        self.id = id
        self.name = '???'
        self.description = ''
        self.contents = []
        self.exits = []
        
    def __repr__(self):
        return '<room {0}: {1}>'.format(self.id, self.name)
        
    def look(self):
        print(self.name)
        print(self.description)
        if len(self.contents) != 0:
            print('Contents: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.contents))))
        if len(self.exits) != 0:
            print('Exits: {0}.'.format(
                ', '.join(map(lambda x: x.name, self.exits)))) 
 
class Exit:
    '''Fields: name (Str), 
               destination (Room)
               key (Thing)
               message (Str)
    '''       
    
    def __init__(self,name,dest):
        self.name = name
        self.destination = dest
        self.key = None
        self.message = ''
        
    def __repr__(self):
        return '<exit {0}>'.format(self.name)

class World:
    '''Fields: rooms ((listof Room)), 
               player (Player)
    '''       
    
    msg_look_fail = "You don't see that here."
    msg_no_inventory = "You aren't carrying anything."
    msg_take_succ = "Taken."
    msg_take_fail = "You can't take that."
    msg_drop_succ = "Dropped."
    msg_drop_fail = "You aren't carrying that."
    msg_go_fail = "You can't go that way."
    
    msg_quit = "Goodbye."
    msg_verb_fail = "I don't understand that."
    
    def __init__(self, rooms, player):
        self.rooms = rooms
        self.player = player

    def look(self, noun):
        '''returns None and prints the name and description of noun, if noun
        does not exist for the current player, "You don't see that here." is 
        printed.
        Effects: prints to the screen
        
        look: World Str -> None
        '''
        inv_names=list(map(lambda x: x.name, self.player.inventory))
        loot_names=list(map(lambda x: x.name, self.player.location.contents))
        if noun=='me':
            Player.look(self.player)
        elif noun=='here':
            Room.look(self.player.location)
        elif noun in inv_names:
            idx=inv_names.index(noun)
            Thing.look(self.player.inventory[idx])
        elif noun in loot_names:
            idx=loot_names.index(noun)
            Thing.look(self.player.location.contents[idx])
        else:
            print(self.msg_look_fail)
        
            
    def inventory(self):
        '''returns None and prints a formatted version of self.player.inventory,
        or prints "You aren't carrying anything." if the inventory is empty.
        Effects: prints to the screen
        
        inventory: World -> None
        '''
        if len(self.player.inventory) != 0:
            print('Inventory: {0}'.format(
                ', '.join(map(lambda x: x.name,self.player.inventory)))) 
        else:
            print(self.msg_no_inventory)
            
    def take(self, noun):
        '''returns None and mutates self.player.location.contents, appends
        self.player.inventory to reflect taking a Thing with name noun from
        self.player.location, then prints "Taken.", or prints "You can't take
        that." if no such Thing is present.
        Effects: mutates self.player.location.contents
                 mutates self.player.inventory
                 prints to the screen
                 
        take: World Str -> None
        '''
        loot_names=list(map(lambda x: x.name, self.player.location.contents))
        if noun in loot_names:
            idx=loot_names.index(noun)
            item=self.player.location.contents[idx]
            self.player.location.contents.pop(idx)
            self.player.inventory.append(item)
            print(self.msg_take_succ)
        else:
            print(self.msg_take_fail)
            
    def drop(self, noun):
        '''returns None and appends self.player.location.contents, mutates
        self.player.inventory to reflect dropping a Thing with name noun from
        self.player.inventory, then prints "Dropped.", or prints "You aren't 
        carrying that." if no such Thing is present.
        Effects: mutates self.player.location.contents
                 mutates self.player.inventory
                 prints to the screen
                 
        drop: World Str -> None
        '''
        inv_names=list(map(lambda x: x.name, self.player.inventory))
        if noun in inv_names:
            idx=inv_names.index(noun)
            item=self.player.inventory[idx]
            self.player.inventory.pop(idx)
            self.player.location.contents.append(item)
            print(self.msg_drop_succ)
        else:
            print(self.msg_drop_fail)        
        
    def go(self, noun):
        '''returns None and mutates self.player.location to the destination of
        the Exit indicated by noun, then looks at the current location of
        self.player, or prints "You can't go that way." if the exit with name
        noun doesn't exist. if the exit requires a key, self.player.location
        will only be updated if the key required is in self.player.inventory,
        or it will print the exit's exit.message.
        Effects: mutates self.player.location
                 prints to the screen
        
        go: World Str -> None
        '''
        exit_names=list(map(lambda x: x.name, self.player.location.exits))
        if noun in exit_names:
            idx=exit_names.index(noun)
            ex=self.player.location.exits[idx]
            if ex.key==None or ex.key in self.player.inventory:
                self.player.location=ex.destination
                Room.look(self.player.location)
            else:
                print(ex.message)
        else:
            print(self.msg_go_fail)
                
    def play(self):
        player = self.player
        
        player.location.look()
        
        while True:
            line = input( "- " )
            
            wds = line.split()
            verb = wds[0]
            noun = ' '.join( wds[1:] )
            
            if verb == 'quit':
                print( self.msg_quit )
                return
            elif verb == 'look':
                if len(noun) > 0:
                    self.look(noun)  
                else:
                    self.look('here')
            elif verb == 'inventory':
                self.inventory()     
            elif verb == 'take':
                self.take(noun)    
            elif verb == 'drop':
                self.drop(noun)
            elif verb == 'go':
                self.go(noun)   
            else:
                print( self.msg_verb_fail )

    ## Q3
    def save(self, fname):
        '''returns None and writes the current state of self to a file called
        fname, which can be used with load to return to the saved world self.
        Effect: writes to file fname
        
        save: World Str -> None
        '''
        # setup
        things=[]
        rooms=self.rooms
        player=self.player
        exits={}
        
        # gather contents of rooms
        for i in range(len(rooms)):
            things.extend(rooms[i].contents)
        
        # gather player inventory
        things.extend(self.player.inventory)
        
        # gather exits
        for r in rooms:
            for e in r.exits:
                exits[e]=str(r.id)
        
        # creating new file for writing
        s=open(fname,'w')
        
        # save things
        for t in things:
            s.write('thing #{0} {1}\n'.format(t.id,t.name))
            s.write(t.description)
            s.write('\n')
            
        # save rooms
        for r in rooms:
            s.write('room #{0} {1}\n'.format(r.id,r.name))
            s.write('{0}\n'.format(r.description))
            s.write('contents')
            content_ids=list(map(
                lambda x: str(x),list(t.id for t in r.contents)))
            if content_ids!=[]:
                s.write(' #')
                s.write(' #'.join(content_ids))
            s.write('\n')
        
        # save player
        s.write('player #{0} {1}\n'.format(player.id,player.name))
        s.write(player.description)
        s.write('\n')
        s.write('inventory')
        inv_ids=list(map(
            lambda x: str(x),list(t.id for t in player.inventory)))
        if inv_ids!=[]:
            s.write(' #')
            s.write(' #'.join(inv_ids))
        s.write('\nlocation #')
        s.write(str(player.location.id))
        s.write('\n')
        
        # save exits
        for e in exits:
            if e.key!=None:
                s.write('keyexit #{0} #{1} {2}\n'.format(
                    exits[e],
                    e.destination.id,
                    e.name))
                s.write('#{0} {1}\n'.format(
                    e.key.id,
                    e.message))
            else:
                s.write('exit #{0} #{1} {2}\n'.format(
                    exits[e],
                    e.destination.id,
                    e.name))
        
        # close file
        s.close()

## Q2
def load(fname):
    '''returns a World constructed from the information given in the text file
    with filename fname
    
    load: Str -> World
    requires: fname points to a file with properly formatted World save data
    '''
    # read file, set up dictionaries
    infile=open(fname,'r')
    data=list(map(lambda x: x.replace('\n',''),infile.readlines()))
    data.append('')
    infile.close()
    things={}
    rooms={}
    pos=0
    
    # things
    while data[pos].split()[0]=='thing':
        line1=data[pos].split()
        num=int(line1[1].replace('#',''))
        name=' '.join(line1[2:])
        description=data[pos+1]
        temp=Thing(num)
        temp.name=name
        temp.description=description
        things[num]=temp
        pos+=2
    
    # rooms 
    while data[pos].split()[0]=='room':
        line1=data[pos].split()
        num=int(line1[1].replace('#',''))
        name=' '.join(line1[2:])
        description=data[pos+1]
        line3=data[pos+2].split()
        con_ids=list(
            map(lambda x: int(x.replace('#','')),line3[1:]))
        contents=list(map(lambda x: things[x],con_ids))
        temp=Room(num)
        temp.name=name
        temp.description=description
        temp.contents.extend(contents)
        rooms[num]=temp
        pos+=3
    
    # player
    pline1=data[pos].split()
    p_id=int(pline1[1].replace('#',''))
    pname=' '.join(pline1[2:])
    pline3=data[pos+2].split()
    inv_ids=list(
        map(lambda x: int(x.replace('#','')),pline3[1:]))
    inventory=list(map(lambda x: things[x],inv_ids))
    player=Player(p_id)
    player.name=pname
    player.description=data[pos+1]
    player.inventory=inventory
    player.location=rooms[int(data[pos+3].split()[1].replace('#',''))]
    pos+=4
    
    # exits
    while data[pos] != '':
        info=data[pos].split()
        name=' '.join(info[3:])
        rnum=int(info[1].replace('#',''))
        dnum=int(info[2].replace('#',''))
        ext=Exit(name,rooms[dnum])
        if info[0]=='keyexit':
            line2=data[pos+1].split()
            key=things[int(line2[0].replace('#',''))]
            msg=' '.join(line2[1:])
            ext.key=key
            ext.message=msg
            pos+=2
        else:
            pos+=1
        rooms[rnum].exits.append(ext)
    
    # build World
    roomlist=list(rooms[j] for j in rooms)
    return World(roomlist,player)
    

def main():
    print('<<<<<<<<turbo cool text adventure game>>>>>>>>')
    print('select a world from below:')
    listf=os.listdir()
    listf.remove('game.py')
    print('>{0}'.format('\n>'.join(listf)))
    
    
if __name__=='__main__':
    main()
    selection=input('>')
    if selection in os.listdir():
        print('\n')
        print('loaded <{0}>\n'.format(selection))
        print('INSTRUCTIONS')
        print('-use "go <exit>" to go to <exit>')
        print('-use "take <item>" or "drop <item>" to take or drop items')
        print('-use "quit" to quit')
        print('-use "game.save(<filename>)" to save after quitting\n\n')
        game=load(selection)
        game.play()    