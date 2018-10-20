for root in ALL_INSTANCES/ALL_INSTANCES_FOLD*; do
  site_number=1
  
  for d in $root/*; do
    site="$(echo $d | rev | cut -d'/' -f 1 | rev)"
 #    echo $site   

    i=1
    for cluster in $d/*; do 
        awk -v x=$site_number '$1=x ' $cluster >> WSC_Eval_simple_TCP_100S_50SP_15ISP_20IMP_${site}_${i}.train

        wc="$(wc -l $cluster)"           
        instances_current_cluster="$(echo $wc | cut -d" " -f 1)"

  #      echo ${site} $i

        
        for site_for_background in $root/*; do
             
            for cluster_for_background in $site_for_background/*;do
              
               if [ "$site_for_background" != "$d" ]; then
                 #  echo "current site "  $d
                 #  echo "site backgro "  $site_for_background
 
                                 
                  cat $cluster_for_background >> temp_${site}_${i}
               fi
            done
        done

        shuf -n $instances_current_cluster temp_${site}_${i} >> background_${site}_${i}

        background_set=background_${site}_${i}
        awk '$1=-1 ' $background_set >> WSC_Eval_simple_TCP_100S_50SP_15ISP_20IMP_${site}_${i}.train   
        
        i=$((i+1))
    done

    site_number=$((site_number + 1))
  done

  fold="$(echo $root | rev | cut -d'_' -f 1 | rev)" 
  echo $fold 
  mkdir ${fold}_train
  mv *.train ${fold}_train
  rm background_*
  rm temp_*
done


#mkdir train_prova
#mv *train train_prova

#mkdir temp_prova
#mv temp_* temp_prova

#mkdir background_prova
#mv background_* background_prova
