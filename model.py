# Creating a regex dict based on the found regular expressions for each objection
import re
regex_dict = {
    "Interested" : ["""(I |we |this |he |she )*(([a-z,'’"]+[^a-z,'’"]*){0,2})(?<!not|n't)(?<!don't think we are)(?<!you're)(?<!you’re)(?<!you be) interested""",
                   """(?<!face)(?<!re)(send |book|schedul)( )*(?<!not )(([a-z,’']+[^a-z,’']*){0,3}) (a |an )*(?<!cancelled )(?<!postpone our )(?<!push the )(?<!internal )(?<!on a short )(?<!have a )(?<!more )(?<!reschedule our )(time|meet|(quick )*call|invite)( with me)*""",
                   """(lets|looking forward|need|let's)[ ]*(to )*(talking|talk|meet)( )*(to )*(you)*"""
                    """(We|we|we’re|We’re|I|I'm)*( is| are| am| be| would)* (both )*(really )*(very )*(?<! not )(want|keen|willing|curious) (to|in|about) (learning|learn|your)*( more| tool)*""",
                    """outplay is (our|my)( preferred| personal) choice""",
                    """(we )*can do (a )*([a-z]*) (call|meet)""",
                    """I would like to speak with you""",
                    """we want to get started"""
     ],
    "Authority" : [
        """(I am|I('|’)m|I|im)*( would)*not( be| in)*( the| a)*( right| concerned| responsible| correct| ultimate| final| best| your)* (guy|(contact )*person|(point of )*contact|position|for that)(?!ally)( you are looking)*""",
        """(I|I'm)*( am not| am also not| don't| do not|not| not)( having| have| take| make)*( any| the| your| a| those| these| such|)( correct| ultimate| final| types of)*( decision making| decision maker| decision-maker| decision)( power)*""",
        """(I )*(don('|’)t|do not) (oversee|look after|manage) (([a-z,'’"]+[^a-z,'’"]*){0,2})""",
        """(This |this )*(is|doesn('|’)t come|does not come) (beyond|not under|under|not really) my (scope|range|control|reach|area)""",
        """(better|good|correct) (person|man) for you"""
    ],
    "Competitor" : [
        """(we|they|we('|’)re)*( are| were| had)*( currently| already| also| just)*( been)*(?<! not)( using( a(n)*)*| implementing| satisfied with)(?! a)(?! an)(?! the)(?! internal)(?! the email)(?! the link )(?! outplay)(?! either)(?! it)(?! our)(?! this)(?! it) [a-z.-]*( engagement (platform|tool)| force| intel| loft| info| campaign)*""",
        """(we're|we are|they are|we have been|i'm|company is)*( decided)*( to)*( very| pretty)* (happy|good|going|partnering)( use| to stick)*( with)(?! that)(?! this)( our)*( the)*( current)* [a-z]*( tool|( engagement)* platform| stack| we use| force| loft| info| campaign| intel)*""",
        """(we|I)*( just| have| are| are)*( already| heavily| extremely)* ((in |new )*contract with|invested)(?! outplay)( on| in our| with| to| in| a lot ((of )*money)*)*( current)* [a-z]*(( number of)* tool(s)*| force| loft| info| campaign| intel)*""",
        """(we're|we are)( currently| all)* (set|ok)""",
        """(we|company)*( recently| just)* (went with|moved to)( a| an)*( new contract with)* ([a-z]*)""",
        """we (are )*(happy |found a better)(([a-z,’']+[^a-z,’']*){0,1})( )*(customers|users|option)""",
        """(we)* (already have) (?!what)(?!a)(?!the)(?!an)*[a-z]*"""
    ],
    "Timing" : [
        """(I('|’)ve|I have|I|we|I('|’)m)*( am|was| was| are| were| been)*( just| rather| pretty| incredibly|( )*super)* (([a-z,’'-]+[^a-z,’'-]*){0,2})( )*(?<!you're )(?<!you are )busy( this)*( scheduled| time| week| schedule)*( with (a |the |that )*([a-z]*))*""",
        """timing (isn('|’)t|is not) (good|right)""",
        """(we're |we are |I'm |I am )*(not |no |n't )(([a-z,’'-]+[^a-z,’']*){0,2})(?<! interested)(?<! budget)(?<! interest) at this time""",
        """at this time (, )*(([a-z,'’]+[^a-z,'’]*){0,2}) (not|no|n't)(?! interest)"""
        """I am not available"""
    ],  
    "Budget" : [
        """no budget""",
        """(do |have |I am |I |we )*(not |don('|’)t |haven(’|')t |dont |havent )(([a-z,'’-]+[^a-z,'’]*){0,3}) (budget|money)""",
        """(budget|budgets) (([a-z,'-’]+[^a-z,'’]*){0,3}) (tight|freeze|frozen)""",
        """(tight|freeze|frozen) (([a-z,'’-]+[^a-z,'’]*){0,3}) budget"""
        """(budget|budgetory) discussion"""
    ],
    "Not Interested" : [
        """(we’re|we are|I’m|I am)*( )*(not|no) (([a-z,'’]+[^a-z,'’]*){0,3})( )*(interested| interest)""",
        """Not (needed|required)""",
        """Stop (mailing|contacting)""",
        """Unsubscribe""",
        """Remove me from your [a-z]*( )*list""",
        """Not looking (for this kind of tool|([a-z,'’]+[^a-z,'’]*){0,3}|)"""
    ]
}

# function to find objections using regex_dict in the new_clean_msg
def identify_objections(text):
    """Identifies objection from a given text
    
    Input:
    new_clean_msg
    text: str
    
    Output
    objections in new_clean_msg
    """
    ans = []
    for label, exp_list in regex_dict.items():
        for exp in exp_list:
            regex_pattern_check = re.search(exp, text, re.IGNORECASE)
            if regex_pattern_check:
                ans.append({
                    'class': label,
                    'evidence': text[regex_pattern_check.start():regex_pattern_check.end()], 
                    'start': regex_pattern_check.start(),
                    'end': regex_pattern_check.end(),
#                     'regex': exp
                })
    return ans

text = """Hi Vamsi - appreciate the prep in your email. At the moment we're using outreach for our outbound engagement. I'm quite tight on time at the minute and not keen to put something in the calendar, but if you want to send me over why outplay would be a step up for us, I'm happy to take a look and come back to you if we're interested in exploring further. Thanks, Clay"""
print(identify_objections(text))