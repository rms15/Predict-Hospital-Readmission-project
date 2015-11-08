function [ test_notok_prob ] = hosp_labtest_train_hmm( seq, iter )
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here

        cum_prob = 0;
        if length(seq) == 0
            test_notok_prob = 0;
        else
            for i = 1:iter
                r1 = rand; r2 = rand;
                aguess = [r1,1-r1; r2,1-r2];
%                bguess = [r1,1-r1;r2,1-r2];
                bguess = [0.9,0.1; 0.1,0.9];
%                [a_est1,b_est1] = hmmtrain(seq,aguess,bguess);
                pStates = hmmdecode(seq,aguess,bguess);
                cum_prob = cum_prob + pStates(2,size(pStates,2));
            end
%            test_notok_prob = cum_prob/iter;
            test_notok_prob = cum_prob/iter;
        end
end

